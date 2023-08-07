import numpy as np
import tensorflow as tf
from .training import ReplayBuffer, LayerSpec
from matplotlib import pyplot as plt

from api.lib.blackjack import Table, Dealer, Player, Shoe, DecisionModel

class QPolicy: 
    def __init__(
        self, 
        state_size, 
        action_size, 
        epsilon, 
        layer_specs = None
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        
        #default layer specs 
        if (layer_specs is None): 
            layer_specs = [
                LayerSpec(24, 'relu'),
                LayerSpec(24, 'relu')
            ]
        
        self.model = self.build_model(layer_specs)
        self.replay_buffer = ReplayBuffer(10000)
        
    def build_model(self, layer_specs):
        model = tf.keras.models.Sequential()
        
        model.add(tf.keras.layers.Dense(layer_specs[0].size, input_dim=self.state_size, activation=layer_specs[0].activation))
        
        for i in range(1, len(layer_specs)): 
            model.add(tf.keras.layers.Dense(layer_specs[i].size, activation=layer_specs[i].activation))
            
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam())
        return model
        
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            #explore: select a random action
            return np.random.choice(2)
        else:
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            q_values = self.model(state_tensor)
            return np.argmax(q_values[0])
    
    def update_epsilon(self, epsilon):
        self.epsilon = epsilon
       
    def update_model(self, batch_size, gamma=0.5):
        if len(self.replay_buffer) < batch_size:
            return
            
        #random sample from replay buffer 
        state, action, reward, next_state, done = self.replay_buffer.sample(batch_size)

        #current & next state 
        state_tensor = tf.convert_to_tensor(state)
        next_state_tensor = tf.convert_to_tensor(next_state)
        
        #convert to q-values with model 
        q_values = self.model(state_tensor)
        q_values_next = self.model(next_state_tensor)

        q_target = reward + gamma * tf.reduce_max(q_values_next, axis=1)
        q_target = tf.where(done, reward, q_target)
        
        indices = tf.range(batch_size)[:, tf.newaxis]
        actions = tf.cast(action, dtype=tf.int32)[:, tf.newaxis]
        indices_actions = tf.concat([indices, actions], axis=1)
        
        q_values = tf.tensor_scatter_nd_update(q_values, indices_actions, q_target)

        #train model 
        self.model.fit(state_tensor, q_values, epochs=1, verbose=0)

    def save_model(self): 
        self.model.save("model/model_saved")
        
    def load_saved_model(self): 
        self.model = tf.keras.models.load_model("model/model_saved")

class QLearningDecisionModel(DecisionModel): 
    def __init__(
        self, 
        use_hi_lo_count: bool = False, 
        normalize_state: bool= False
    ): 
        self.use_hi_lo_count = use_hi_lo_count
        self.normalize_state = normalize_state
        self.policy = {}
        
        #initialize policy to all False 
        for showing in range(1, 12): 
            self.policy[showing] = { }
            for ace_count in range(0, 4): 
                self.policy[showing][ace_count] = { }
                for p_hand in range(2, 21): 
                    self.policy[showing][ace_count][p_hand] = False
        
    def update_policy(self, state, value: bool): 
        showing = state[0]
        p_hand = state[1]
        ace_count = state[2]
        
        if (ace_count > 3): 
            ace_count = 3
        
        self.policy[showing][ace_count][p_hand] = value
        
    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        showing = dealer.showing
        player = players[player_index]
        ace_count = player.hand.soft_ace_count
        if (ace_count > 3): 
            ace_count = 3
        
        p_hand = player.hand.total
        return self.policy[showing][ace_count][p_hand]
    
class TrainingEpisode: 
    def __init__(
        self, 
        batch_size: int, 
        num_decks: int, 
        gamma: float, 
        policy: QPolicy,
        num_games: int = 1000,
        update_freq: int = 5, 
        top_up_rate: float = 0.3, 
        use_hi_lo_count: bool = False,
        normalize_state: bool = False
    ): 
        self.policy = policy
        self.batch_size = batch_size
        self.player = Player(QLearningDecisionModel(policy, use_hi_lo_count, normalize_state))
        self.table = Table(Dealer(), num_decks=num_decks, top_up_rate=top_up_rate)
        self.table.add_player(self.player)
        self.prev_state = None
        self.gamma = gamma
        self.iteration_count = 0
        self.update_freq = update_freq
        self.use_hi_lo_count = use_hi_lo_count
        self.normalize_state = normalize_state
        self.num_games = num_games
        
    def update_player_policy(self): 
        self.policy.get_action()
    
    def run(self): 
        
        #fill player policy with values 
        self.update_player_policy()
        
        for i in range(self.num_games): 
        
            #check if need to top up shoe 
            self.table.shoe.auto_top_up()
        
            #deal initial hands 
            self.table.deal_hands()
            self.table.play_round()
    
        reward = self.player.balance
        
class Trainer: 
    def __init__(
        self, 
        num_episodes: int, 
        batch_size: int = 64,
        start_epsilon: float = 1.0,
        end_epsilon: float = 0.01,
        gamma: float = 0.5,
        layer_specs = None, 
        update_freq: int = 5, 
        num_decks: int = 120, 
        top_up_rate: float = 0.3,
        use_hi_lo_count: bool = False, 
        report_interval: int = 100
    ): 
        self.num_episodes = num_episodes
        self.batch_size = batch_size
        self.layer_specs = layer_specs
        self.gamma = gamma
        self.update_freq = update_freq
        self.state_size = 3 if not use_hi_lo_count else 4
        self.action_size = 2
        self.num_decks = num_decks
        self.top_up_rate = top_up_rate
        self.report_interval = report_interval
        self.use_hi_lo_count = use_hi_lo_count

        #decaying epsilon
        self.start_epsilon = start_epsilon
        self.end_epsilon = end_epsilon
        
    def train(
        self,
        load_from_file: bool = False, 
        save_to_file: bool = False
    ): 
        epsilon_decay_duration = (self.num_episodes) // 2
        policy = QPolicy(
            state_size=self.state_size, 
            action_size=self.action_size, 
            epsilon=self.start_epsilon, 
            layer_specs=self.layer_specs
        )
        
        if (load_from_file): 
            policy.load_saved_model()

        results = []
        averages = []
        super_averages = []
        
        for episode in range (self.num_episodes): 
            train = TrainingEpisode(
                num_decks=self.num_decks,
                batch_size=self.batch_size, 
                gamma=self.gamma,
                update_freq=self.update_freq,
                policy=policy, 
                top_up_rate=self.top_up_rate, 
                use_hi_lo_count=self.use_hi_lo_count, 
                normalize_state=self.normalize_state
            )

            # Training loop
            train.run()
                
            # Decay epsilon
            if episode < epsilon_decay_duration:
                policy.update_epsilon(self.end_epsilon + (self.start_epsilon - self.end_epsilon) * ((epsilon_decay_duration - episode) / epsilon_decay_duration))

            prev = 0
            if (len(results) > 0): 
                prev = results[len(results)-1]
                
            results.append(train.player.balance + prev)
            averages.append(train.player.balance / self.num_episodes)
            
            if (episode > 0 and episode % self.report_interval == 0):
                super_averages.append(sum(averages[-self.report_interval:])/self.report_interval)
                
                print(f'epoch {episode}...')
                print('results')
                plt.plot(results)
                plt.show()
                print('averages')
                plt.plot(averages)
                plt.show()
                print('super_averages')
                plt.plot(super_averages)
                plt.show()
                
                if (save_to_file):
                    policy.save_model()
            
        print('Training complete.')
        
        return {
            'results': results, 
            'averages': averages, 
            'super_averages': super_averages
        }
        