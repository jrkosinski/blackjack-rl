import numpy as np
import tensorflow as tf
import random
from tensorflow import keras

from lib.Blackjack import Table, Dealer, Player, Shoe, DecisionModel

class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = map(np.stack, zip(*batch))
        return state, action, reward, next_state, done

    def __len__(self):
        return len(self.buffer)
        
class DQNAgent: 
    def __init__(self, state_size, action_size, epsilon):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.model = self.build_model()
        self.replay_buffer = ReplayBuffer(10000)
        
    def build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam())
        return model
        
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            #explore: select a random action
            return np.random.choice(2)
        else:
            #exploit: select the action with max Q-value
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            q_values = self.model(state_tensor)
            return np.argmax(q_values[0].numpy())
    
    def update_epsilon(self, epsilon):
        self.epsilon = epsilon
        
    def update_model(self, batch_size, gamma=0.5):
        if len(self.replay_buffer) < batch_size:
            return
        state, action, reward, next_state, done = self.replay_buffer.sample(batch_size)

        state_tensor = tf.convert_to_tensor(state)
        next_state_tensor = tf.convert_to_tensor(next_state)
        
        q_values = self.model(state_tensor)
        q_values_next = self.model(next_state_tensor)

        q_target = reward + gamma * tf.reduce_max(q_values_next, axis=1)
        q_target = tf.where(done, reward, q_target)
        
        indices = tf.range(batch_size)[:, tf.newaxis]
        actions = tf.cast(action, dtype=tf.int32)[:, tf.newaxis]
        indices_actions = tf.concat([indices, actions], axis=1)
        
        q_values = tf.tensor_scatter_nd_update(q_values, indices_actions, q_target)

        self.model.fit(state_tensor, q_values, epochs=1, verbose=0)

    def save_model(self): 
        self.model.save_weights("model_saved")
        
class QLearningDecisionModel(DecisionModel): 
    def __init__(self, agent: DQNAgent): 
        self.agent = agent
        
    def decide_hit(self, dealer: Dealer, shoe: Shoe, players, player_index: int):
        soft_ace_count = players[player_index].hand.soft_ace_count
        if (soft_ace_count > 2): 
            soft_ace_count = 2
            
        state = [
            dealer.showing, 
            players[player_index].hand.total,
            soft_ace_count
        ]
        
        return self.agent.get_action(state)

class TrainingEpisode: 
    def __init__(self, batch_size: int, num_decks: int, agent: DQNAgent): 
        self.agent = agent
        self.batch_size = batch_size
        self.player = Player(QLearningDecisionModel(agent))
        self.table = Table(Dealer(), num_decks)
        self.table.add_player(self.player)
        self.prev_state = None
        
    def run(self): 
        self.table.deal_hands()
        
        self.prev_state = self._get_current_state()
        player_start_balance = self.player.balance
        
        def on_game_action(player: Player, done: bool): 
            next_state = self._get_current_state()
            reward = player.balance - player_start_balance
            self.agent.replay_buffer.push(self.prev_state, player.last_action, reward, next_state, done)
            self.prev_state = next_state
            
            self.agent.update_model(self.batch_size)
            
        self.table.on_action(on_game_action)
        self.table.dealer.play_round(self.table.shoe, self.table.players, on_game_action)
        self.table.dealer.assess_winners(self.table.players, on_game_action)
    
    def _get_current_state(self): 
        #TODO: this code is duplicated 
        soft_ace_count = self.player.hand.soft_ace_count
        if (soft_ace_count > 2): 
            soft_ace_count = 2
            
        state = [
            self.table.dealer.showing, 
            self.player.hand.total,
            soft_ace_count
        ]
        
        return state
        

num_episodes = 100
num_epochs = 100
batch_size = 64

#decaying epsilon
start_epsilon = 1.0
end_epsilon = 0.01

epsilon_decay_duration = (num_episodes * num_epochs) // 2
agent = DQNAgent(state_size=3, action_size=2, epsilon=start_epsilon)

for epoch in range (num_epochs): 
    ep = TrainingEpisode(num_decks=12, batch_size=batch_size, agent=agent)

    # Training loop
    for episode in range(num_episodes):
        ep.run()
        
        # Decay epsilon
        if episode < epsilon_decay_duration:
            agent.update_epsilon(end_epsilon + (start_epsilon - end_epsilon) * ((epsilon_decay_duration - episode) / epsilon_decay_duration))

    agent.save_model()
print('Training complete.')

agent.save_model()