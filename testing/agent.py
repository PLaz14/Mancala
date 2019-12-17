# import keras
# import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import gym


def testaimnist():
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dense(10, activation="softmax"))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    model.fit(x_train, y_train, epochs=6)

    # plt.imshow(x_train[0], cmap = plt.cm.binary)
    # plt.show()
    # print(x_train[0])
    predictions = model.predict([x_train])
    print(np.argmax(predictions[0]))
    plt.imshow(x_train[0])
    plt.show()


def testaimountcar():
    env = gym.make("MountainCar-v0")
    env.reset()

    LEARNING_RATE = 0.1
    DISCOUNT = 0.95
    EPISODES = 2000

    SHOW_EVERY = 500

    DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
    discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

    epsilon = 0.5
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = EPISODES // 2
    epsilon_decay_value = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

    ep_rewards = []
    aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

    for episode in range(EPISODES):
        episode_reward = 0
        if episode % SHOW_EVERY == 0:
            render = True
        else:
            render = False
        discrete_state = get_discrete_state(env.reset(), env, discrete_os_win_size)
        done = False
        while not done:
            if np.random.random() > epsilon:
                action = np.argmax(q_table[discrete_state])
            else:
                action = np.random.randint(0, env.action_space.n)
            new_state, reward, done, _ = env.step(action)
            episode_reward += reward
            new_discrete_state = get_discrete_state(new_state, env, discrete_os_win_size)
            if render:
                env.render()
            if not done:
                max_future_q = np.max(q_table[new_discrete_state])
                current_q = q_table[discrete_state + (action,)]
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                q_table[discrete_state + (action,)] = new_q
            elif new_state[0] >= env.goal_position:
                print(f"{episode}")
                q_table[discrete_state + (action,)] = 0

            discrete_state = new_discrete_state
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value
        ep_rewards.append(episode_reward)
        if not episode % SHOW_EVERY:
            average_reward = sum(ep_rewards[-SHOW_EVERY:]) / len(ep_rewards[-SHOW_EVERY:])
            aggr_ep_rewards['ep'].append(episode)
            aggr_ep_rewards['avg'].append(average_reward)
            aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
            aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))

            print(
                f"episode: {episode} avg: {average_reward} min: {min(ep_rewards[-SHOW_EVERY:])} max: {max(ep_rewards[-SHOW_EVERY:])}")

    env.close()
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label='avg')
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label='min')
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label='max')
    plt.legend(loc=4)
    plt.show()


def get_discrete_state(state, env, dows):
    discrete_state = (state - env.observation_space.low) / dows
    return tuple(discrete_state.astype(np.int))


if __name__ == "__main__":
    testaimountcar()
