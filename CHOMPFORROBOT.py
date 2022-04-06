#!/usr/bin/env python
# coding: utf-8

# In[4]:


from Game import *
from RobotSim373 import *


# In[5]:


def initial_state():
    state=Board(4,5)
    
    for i in range(20):
        state [i]=1


    
    return state


# In[6]:


def update_state(state,player,move):
    #a move is a start and end location
    new_state=state
    
    start_row,start_col=state.rc_from_index(move)
    
    for c in range(start_col,5):
        for r in range(start_row,4):
            new_state[r,c]=0
    
    return new_state


# In[7]:


def show_state(state):
    print(state)


# In[8]:


def valid_moves(state,player):
    moves=[]
    for location in range(20):
        if state[location]==1:
            moves.append(location)
    return moves


# In[9]:


def win_status(state,player):
    if state[0]==0:
        return "lose"


# In[10]:


def random_move(state,player):
    moves=valid_moves(state,player)
    moves.remove(0)

    if not moves:
        return 0
    else:
        return random.choice(moves)


# In[11]:


def human_move(state,player):
    
    state.show_locations()
    move=int(input("What square do you want to eat?"))
    
    
    return move
random_agent=Agent(random_move)
human_agent=Agent(human_move)


# In[12]:


from Game.minimax import*
def minimax_move(state,player):
    values,moves=minimax_values(state,player,display=True)
    return top_choice(moves,values)

minimax_agent=Agent(minimax_move)


# In[13]:


def skittles_move(state, player, info):
    T=info.T
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    if state not in T:
        actions=valid_moves(state,player)
        T[state]=Table()
        for action in actions:
            T[state][action]=2 #initial number of skittles
    
    move=weighted_choice(T[state])
    
    if move is None:
        # learn
        if learning:
            if last_state:
                T[last_state][last_action]-=1 #take away a skittle
                if T[last_state][last_action]<0:
                    T[last_state][last_action]=0
        
        return random_move(state,player)
    else:
        return move


# In[14]:


def skittles_after(status,player,info):
    #not return anything but
    #will adjust the skittles table if lost the game
    T=info.T
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    if status=='lose':
        T[last_state][last_action]-=1 #take away a skittle
        if T[last_state][last_action]<0:
            T[last_state][last_action]=0


# In[15]:


def Q_move(state,player,info):
    Q=info.Q
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    
    α=info.α  # learning rate
    ϵ=info.ϵ  # how often to take a random move
    γ=info.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)
    
    # \alpha <hit tab>    α
    # \epsilon <hit tab>  ϵ
    # \gamma <hit tab>    γ
    
    if state not in Q:
        actions=valid_moves(state,player)
        Q[state]=Table()
        for action in actions:
            Q[state][action]=0  # initial value of table
    
    
    if random.random()<ϵ:  # take a random move occasionally to explore the environment
        move=random_move(state,player)
    else:
        move=top_choice(Q[state])
    
    if not last_action is None:  # not the first move
        reward=0
        
        # learn
        if learning:
            Q[last_state][last_action]+=α*(reward +
                        γ*max([Q[state][a] for a in Q[state]]) - Q[last_state][last_action])
    
    return move


# In[16]:


def Q_after(status,player,info):
    Q=info.Q
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    
    α=info.α  # learning rate
    ϵ=info.ϵ  # how often to take a random move
    γ=info.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)
    
    # \alpha <hit tab>    α
    # \epsilon <hit tab>  ϵ
    # \gamma <hit tab>    γ

    if status=='lose':
        reward=-1
    elif status=='win':
        reward=1
    elif status=='stalemate':
        reward=.5 # value stalemate a little closer to a win
    else:
        reward=0
    
    
    if learning:
        Q[last_state][last_action]+=α*(reward - Q[last_state][last_action])


# In[17]:


def build(robot):
    Box(robot,x=5,y=8,width=2,height=30,name="Bar")
    
#     left=Box(robot,x=x-2,y=y,width=.1,height=3,name="left")
#     right=Box(robot,x=x+2,y=y,width=.1,height=3,name="right")
#     connect(disk_center,left,'weld')
#     connect(disk_center,right,'weld')
    
    
    
    robot.boxes=[]
    y=24
    for i in range(4):
        y+=6.45
        box=Box(robot,x=85,y=y,width=3,height=3,angle=180,name="Box %d" % i)
        robot.boxes.append(box)


# In[18]:


def forward(t,robot):
    for disk in robot.boxes:
        disk.F=0
    robot['disk 0'].F=10
    return True


# In[19]:


def wait2(t,robot):
    if t>2:
        return True


# In[20]:


def wait3(t,robot):
    if t>3:
        return True


# In[21]:


def up(t,robot):
    for box in robot.box:
        box.F=0
        
    robot['disk 90'].F=10
    return True


# In[22]:


def monitor(t,robot):
    robot.message=t


# In[23]:


def turn_green(t,robot):
    robot.color='g'
    return True


# In[24]:


def turn_red(t,robot):
    robot.color='r'
    return True


# In[25]:


def turn_purple(t,robot):
    robot.color='purple'
    return True


# In[26]:


def read_distances(t,robot):
    robot.box_distances=[box.read_distance() for box in robot.boxes]
    state=Board(5,4)
    return True


# In[31]:


def get_move(t,robot):
    state=Board(5,4)
    robot.state=state
    robot.move=minimax_move(state,1)
    return True


# In[28]:


def set_move(t,robot):
    count=0
    for distance in robot.box_distances:
        if distance<20:
            count+=1
            
    robot.count=count
    robot.move=(count-1)%4
    if robot.move==0:
        robot.move=1
        
    return True


# In[29]:


def make_move(t,robot):
    move=robot.move
    
    if move==4 and robot.state[3]:  # something in location 3
        return appear_at_4
    else:
        return forward_state_machines[move]


# In[ ]:




