# Dependencies
import math
from time import time
import numpy as np
import torch
from node import Node
from chess_handler import ChessStateHandler
from state_handler.state import StateHandler
import random
from neural_network import NeuralNet


def monte_carlo_tree_search(root: Node, state_handler: StateHandler, policy, max_itr=0, max_time=0) -> Node:
    """
    Runs the monte carlo tree search algorithm.
    If max_itr is 0, it will run until max_time is reached, else it will run for max_itr iterations.
    Returns the root node of the tree generated with the given root.
    """
    if max_itr == 0:
        start_time = time.time()
        while time.time() - start_time < max_time:
            chosen_node: Node = selection(root)
            created_node = expansion(chosen_node, state_handler)
            result = simulation(created_node)
            backpropagation(created_node, result)
    else:
        itr = 0
        while itr < max_itr:
            chosen_node: Node = selection(root)
            created_node = expansion(chosen_node, state_handler)
            result = simulation(created_node)
            backpropagation(created_node, result)
            itr += 1

    return root


def selection(node: Node) -> Node:
    '''
    This selects the best leaf for expansion.
    For Monte Carlo this is the node that you should expand.
    Given by exploration and exploitation means.
    '''
    child_nodes = node.get_children()
    best_child = None
    best_node_value = 0

    while child_nodes:
        for child_node in child_nodes:
            if (best_node_value < ucb(child_node)):
                best_child = child_node
                best_node_value = ucb(child_node)
        return selection(best_child)
    return node


def expansion(node: Node, state_handler: StateHandler) -> Node:
    """
    Generates a new child to node. It is generated by making a random move, 
    checking if that move has a corresponding child, if not it generates a child with the random move.
    Repeats until a child is generated
    """
    moves = state_handler.get_legal_actions()
    # TODO: Make child for each move
    print("Node state: \n", node.get_state())
    for move in moves:
        virtual_state_handler = state_handler.move_to_state()
        state_handler.step(move)

        child_state = state_handler.get_state()
        # Make the child node and make it a child of the input node
        # Problem: the state is not set correctly for the child node
        print()
        # print("Child state: ", child_state)
        child_node = Node(child_state)
        node.add_child(child_node)
        print("Child node: \n", child_node.get_state())
        state_handler.step_back()
        print("")
    # TODO: Make use of default policy
    if node.get_children():
        return random.choice(node.get_children())
    else:
        return node


# def defaultPolicy(game: StateHandler, model=None):
#     '''
#     choosing moves in simulations/rollout
#     '''
#     if model != None:
#         model_prediction: torch.Tensor = model(game.get_state())
#         np_arr: np.array = model_prediction.detach().numpy()
#         best_move = np.argmax(np_arr)
#         best_move += 1
#         return best_move
#     else:
#         return choose_move(game.get_legal_actions())


def choose_move(legal_actions: list):
    """"
    Takes in legal moves an chooses one of them at random
    """
    index = random.randint(0, len(legal_actions)-1)
    move = legal_actions[index]
    return move


def simulation(node: Node) -> int:
    """
    In this process, a simulation is performed by choosing moves or strategies until a result or predefined state is achieved.
    """
    state = node.get_state()
    while state.is_finished():
        legal_action = state.get_legal_actions()
        state.step(choose_move(legal_action))  # TODO refactor

    return state.get_winner()


def backpropagation(node: Node, result: int) -> None:
    """
    After determining the value of the newly added node, the remaining tree must be updated. 
    So, the backpropagation process is performed, where it backpropagates from the new node to the root node. 
    During the process, the number of simulation stored in each node is incremented. Also, if the new node’s 
    simulation results in a win, then the number of wins is also incremented.
    """
    node.add_visits()
    node.add_reward(result)
    if not node.is_root():  # if node is not root, then it has a parent and backpropagates to it
        backpropagation(node.get_parent(), -result)

def ucb(node: Node):
    """
    Takes in node and returns upper confidence bound based on parent node visits and node visits
    """
    exploration_parameter = math.sqrt(2)
    exploitation = node.get_wins()/node.get_visits()
    exploration = np.sqrt(
        np.log(node.get_parent().get_visits())/node.get_visits())
    return exploitation + exploration_parameter*exploration

def generate_test_data(start_node: Node, num_games: int, sims_pr_game: int, board_size: int, model: NeuralNet = None):
    # start_node = start_node
    for i in range(num_games):
        node = Node(start_node.getState())
        game = HexHandler(board_size)
        monte = MCTS(game, node)
        # print("Iteration: " + str(i))
        while not game.is_finished() and node != None:
            # print()
            # print("Running tree search")
            monte.runTreeSearch(sims_per_game, model)
            player = game.getCurrentPlayer()
            state = [node.getState()]
            state = np.asarray(state)
            state = np.insert(state, 0, player)
            # print("state: " + str(state))
            distribution = MCTS.getActionProb(node)
            distribution = np.asarray(distribution, dtype=np.float32)
            # print("state: " + str(state) + " distribution: " + str(distribution))
            GameData.addData(state, distribution)
            best_move_node = MCTS.getBestMove(node)
            game.moveToState(best_move_node)
            # Update the root node to the best_move_node
            monte.root = best_move_node
            node = best_move_node

def get_action_probabilities(node: Node) -> list:
    """
    Finds the best move to be done by Monte Carlo by Node.
    Should return
    """
    result = []
    #softmax of result

    return result





if __name__ == "__main__":
    game = ChessStateHandler()
    node = Node(game.get_state())

    expanded_node = expansion(node, game)
    print("Amount of children: ", len(node.get_children()))
    for child in node.get_children():
        print("=====================================")
        print(child.get_state())
    print("=====================================")
    print(expanded_node.get_state())