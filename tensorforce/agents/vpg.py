# Copyright 2018 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from tensorforce.agents import PolicyAgent


class VanillaPolicyGradient(PolicyAgent):
    """
    [Vanilla Policy Gradient](https://link.springer.com/article/10.1007/BF00992696) aka REINFORCE
    agent (specification key: `vpg`).

    Args:
        states (specification): States specification
            (<span style="color:#C00000"><b>required</b></span>), arbitrarily nested dictionary of
            state descriptions (usually taken from `Environment.states()`) with the following
            attributes:
            <ul>
            <li><b>type</b> (<i>"bool" | "int" | "float"</i>) &ndash; state data type
            (<span style="color:#00C000"><b>default</b></span>: "float").</li>
            <li><b>shape</b> (<i>int | iter[int]</i>) &ndash; state shape
            (<span style="color:#C00000"><b>required</b></span>).</li>
            <li><b>num_states</b> (<i>int > 0</i>) &ndash; number of discrete state values
            (<span style="color:#C00000"><b>required</b></span> for type "int").</li>
            <li><b>min_value/max_value</b> (<i>float</i>) &ndash; minimum/maximum state value
            (<span style="color:#00C000"><b>optional</b></span> for type "float").</li>
            </ul>
        actions (specification): Actions specification
            (<span style="color:#C00000"><b>required</b></span>), arbitrarily nested dictionary of
            action descriptions (usually taken from `Environment.actions()`) with the following
            attributes:
            <ul>
            <li><b>type</b> (<i>"bool" | "int" | "float"</i>) &ndash; action data type
            (<span style="color:#C00000"><b>required</b></span>).</li>
            <li><b>shape</b> (<i>int > 0 | iter[int > 0]</i>) &ndash; action shape
            (<span style="color:#00C000"><b>default</b></span>: scalar).</li>
            <li><b>num_actions</b> (<i>int > 0</i>) &ndash; number of discrete action values
            (<span style="color:#C00000"><b>required</b></span> for type "int").</li>
            <li><b>min_value/max_value</b> (<i>float</i>) &ndash; minimum/maximum action value
            (<span style="color:#00C000"><b>optional</b></span> for type "float").</li>
            </ul>
        max_episode_timesteps (int > 0): Maximum number of timesteps per episode
            (<span style="color:#00C000"><b>default</b></span>: not given).

        network ("auto" | specification): Policy network configuration, see
            [networks](../modules/networks.html)
            (<span style="color:#00C000"><b>default</b></span>: "auto", automatically configured
            network).

        batch_size (parameter, long > 0): Number of episodes per update batch
            (<span style="color:#00C000"><b>default</b></span>: 10 episodes).
        update_frequency ("never" | parameter, long > 0): Frequency of updates
            (<span style="color:#00C000"><b>default</b></span>: batch_size).
        learning_rate (parameter, float > 0.0): Optimizer learning rate
            (<span style="color:#00C000"><b>default</b></span>: 3e-4).

        discount (parameter, 0.0 <= float <= 1.0): Discount factor for future rewards of
            discounted-sum reward estimation
            (<span style="color:#00C000"><b>default</b></span>: 0.99).
        estimate_terminal (bool): Whether to estimate the value of terminal states
            (<span style="color:#00C000"><b>default</b></span>: false).

        baseline_network ("same" | "equal" | specification): Baseline network configuration, see
            [networks](../modules/networks.html), "same" refers to reusing the main network as part
            of the baseline policy, "equal" refers to using the same configuration as the main
            network
            (<span style="color:#00C000"><b>default</b></span>: none).
        baseline_optimizer ("same" | float > 0.0 | "equal" | specification): Baseline optimizer
            configuration, see [optimizers](../modules/optimizers.html), "same"
            refers to reusing the main optimizer for the baseline, a float implies "same" and
            specifies the weight for the baseline loss (otherwise 1.0), "equal" refers to using the
            same configuration as the main optimizer
            (<span style="color:#00C000"><b>default</b></span>: none).

        preprocessing (dict[specification]): Preprocessing as layer or list of layers, see
            [preprocessing](../modules/preprocessing.html), specified per state-type or -name and
            for reward
            (<span style="color:#00C000"><b>default</b></span>: none).

        exploration (parameter | dict[parameter], float >= 0.0): Exploration, global or per action,
            defined as the probability for uniformly random output in case of `bool` and `int`
            actions, and the standard deviation of Gaussian noise added to every output in case of
            `float` actions (<span style="color:#00C000"><b>default</b></span>: 0.0).
        variable_noise (parameter, float >= 0.0): Standard deviation of Gaussian noise added to all
            trainable float variables (<span style="color:#00C000"><b>default</b></span>: 0.0).

        l2_regularization (parameter, float >= 0.0): Scalar controlling L2 regularization
            (<span style="color:#00C000"><b>default</b></span>:
            0.0).
        entropy_regularization (parameter, float >= 0.0): Scalar controlling entropy
            regularization, to discourage the policy distribution being too "certain" / spiked
            (<span style="color:#00C000"><b>default</b></span>: 0.0).

        name (string): Agent name, used e.g. for TensorFlow scopes
            (<span style="color:#00C000"><b>default</b></span>: "agent").
        device (string): Device name
            (<span style="color:#00C000"><b>default</b></span>: TensorFlow default).
        parallel_interactions (int > 0): Maximum number of parallel interactions to support,
            for instance, to enable multiple parallel episodes, environments or (centrally
            controlled) agents within an environment
            (<span style="color:#00C000"><b>default</b></span>: 1).
        buffer_observe (bool | int > 0): Maximum number of timesteps within an episode to buffer
            before executing internal observe operations, to reduce calls to TensorFlow for
            improved performance
            (<span style="color:#00C000"><b>default</b></span>: max_episode_timesteps or 1000,
            unless summarizer specified).
        seed (int): Random seed to set for Python, NumPy and TensorFlow
            (<span style="color:#00C000"><b>default</b></span>: none).
        execution (specification): TensorFlow execution configuration with the following attributes
            (<span style="color:#00C000"><b>default</b></span>: standard): ...
        saver (specification): TensorFlow saver configuration with the following attributes
            (<span style="color:#00C000"><b>default</b></span>: no saver):
            <ul>
            <li><b>directory</b> (<i>path</i>) &ndash; saver directory
            (<span style="color:#C00000"><b>required</b></span>).</li>
            <li><b>filename</b> (<i>string</i>) &ndash; model filename
            (<span style="color:#00C000"><b>default</b></span>: "model").</li>
            <li><b>frequency</b> (<i>int > 0</i>) &ndash; how frequently in seconds to save the
            model (<span style="color:#00C000"><b>default</b></span>: 600 seconds).</li>
            <li><b>load</b> (<i>bool | str</i>) &ndash; whether to load the existing model, or
            which model filename to load
            (<span style="color:#00C000"><b>default</b></span>: true).</li>
            </ul>
            <li><b>max-checkpoints</b> (<i>int > 0</i>) &ndash; maximum number of checkpoints to
            keep (<span style="color:#00C000"><b>default</b></span>: 5).</li>
        summarizer (specification): TensorBoard summarizer configuration with the following
            attributes (<span style="color:#00C000"><b>default</b></span>: no summarizer):
            <ul>
            <li><b>directory</b> (<i>path</i>) &ndash; summarizer directory
            (<span style="color:#C00000"><b>required</b></span>).</li>
            <li><b>frequency</b> (<i>int > 0, dict[int > 0]</i>) &ndash; how frequently in
            timestepsto record summaries, applies to "variables" and "act" if specified globally
            (<span style="color:#00C000"><b>default</b></span>:
            always), otherwise specified per "variables"/"act" in timesteps and "observe"/"update"
            in updates (<span style="color:#00C000"><b>default</b></span>: never).</li>
            <li><b>flush</b> (<i>int > 0</i>) &ndash; how frequently in seconds to flush the
            summary writer (<span style="color:#00C000"><b>default</b></span>: 10).</li>
            <li><b>max-summaries</b> (<i>int > 0</i>) &ndash; maximum number of summaries to keep
            (<span style="color:#00C000"><b>default</b></span>: 5).</li>
            <li><b>labels</b> (<i>"all" | iter[string]</i>) &ndash; all or list of summaries to
            record, from the following labels
            (<span style="color:#00C000"><b>default</b></span>: only "graph"):</li>
            <li>"distributions" or "bernoulli", "categorical", "gaussian", "beta":
            distribution-specific parameters</li>
            <li>"dropout": dropout zero fraction</li>
            <li>"entropy": entropy of policy distribution</li>
            <li>"graph": graph summary</li>
            <li>"kl-divergence": KL-divergence of previous and updated policy distribution</li>
            <li>"losses" or "loss", "objective-loss", "regularization-loss", "baseline-loss",
            "baseline-objective-loss", "baseline-regularization-loss": loss scalars</li>
            <li>"parameters": parameter scalars</li>
            <li>"relu": ReLU activation zero fraction</li>
            <li>"rewards" or "timestep-reward", "episode-reward", "raw-reward", "processed-reward",
            "estimated-reward": reward scalar
            </li>
            <li>"update-norm": update norm</li>
            <li>"updates": update mean and variance scalars</li>
            <li>"updates-full": update histograms</li>
            <li>"variables": variable mean and variance scalars</li>
            <li>"variables-full": variable histograms</li>
            </ul>
        recorder (specification): Experience traces recorder configuration with the following
            attributes (<span style="color:#00C000"><b>default</b></span>: no recorder):
            <ul>
            <li><b>directory</b> (<i>path</i>) &ndash; recorder directory
            (<span style="color:#C00000"><b>required</b></span>).</li>
            <li><b>frequency</b> (<i>int > 0</i>) &ndash; how frequently in episodes to record
            traces (<span style="color:#00C000"><b>default</b></span>: every episode).</li>
            <li><b>max-traces</b> (<i>int > 0</i>) &ndash; maximum number of traces to keep
            (<span style="color:#00C000"><b>default</b></span>: all).</li>
    """

    def __init__(
        # Environment
        self, states, actions, max_episode_timesteps,
        # Network
        network='auto',
        # Optimization
        batch_size=10, update_frequency=None, learning_rate=3e-4,
        # Reward estimation
        discount=0.99, estimate_terminal=False,
        # Baseline
        baseline_network=None, baseline_optimizer=1.0,
        # Preprocessing
        preprocessing=None,
        # Exploration
        exploration=0.0, variable_noise=0.0,
        # Regularization
        l2_regularization=0.0, entropy_regularization=0.0,
        # TensorFlow etc
        name='agent', device=None, parallel_interactions=1, seed=None, execution=None, saver=None,
        summarizer=None, recorder=None, config=None
    ):
        memory = dict(type='recent', capacity=((batch_size + 1) * max_episode_timesteps))
        if update_frequency is None:
            update = dict(unit='episodes', batch_size=batch_size)
        else:
            update = dict(unit='episodes', batch_size=batch_size, frequency=update_frequency)
        optimizer = dict(type='adam', learning_rate=learning_rate)
        objective = 'policy_gradient'
        if baseline_network is None:
            reward_estimation = dict(horizon='episode', discount=discount)
            baseline_policy = None
            assert baseline_optimizer == 1.0
            baseline_optimizer = None
            baseline_objective = None
        else:
            reward_estimation = dict(
                horizon='episode', discount=discount,
                estimate_horizon=('late' if estimate_terminal else False),
                estimate_terminal=estimate_terminal, estimate_advantage=True
            )
            # State value doesn't exist for Beta
            baseline_policy = dict(network=baseline_network, distributions=dict(float='gaussian'))
            baseline_objective = 'state_value'

        super().__init__(
            # Agent
            states=states, actions=actions, max_episode_timesteps=max_episode_timesteps,
            parallel_interactions=parallel_interactions, buffer_observe=True, seed=seed,
            recorder=recorder, config=config,
            # Model
            name=name, device=device, execution=execution, saver=saver, summarizer=summarizer,
            preprocessing=preprocessing, exploration=exploration, variable_noise=variable_noise,
            l2_regularization=l2_regularization,
            # PolicyModel
            policy=None, network=network, memory=memory, update=update, optimizer=optimizer,
            objective=objective, reward_estimation=reward_estimation,
            baseline_policy=baseline_policy, baseline_network=None,
            baseline_optimizer=baseline_optimizer, baseline_objective=baseline_objective,
            entropy_regularization=entropy_regularization
        )
