import networkx as nx
import matplotlib.pyplot as plt
import random
from vk_api.exceptions import ApiError
import vk_api

def getFriendsInfo(vk, user_id):
    try:
        friends = vk.friends.get(user_id=user_id, fields="bdate,city")['items']
        friends_data = []
        for friend in friends:
            name = f"{friend['first_name']} {friend['last_name']}"
            age = friend.get('bdate', 'N/A')
            city = friend.get('city', {}).get('title', 'N/A')
            friends_data.append({'name': name, 'age': age, 'city': city})
        return friends_data
    except ApiError as e:
        # print(f"Ошибка API: {e}")
        return []

def createSocialGraph(friends_data):
    G = nx.Graph()
    for friend in friends_data:
        G.add_node(friend['name'], age=friend['age'], city=friend['city'])
        for other_friend in friends_data:
            if friend != other_friend and random.random() < 0.1:
                G.add_edge(friend['name'], other_friend['name'])
    return G

def plotGraph(G, show_labels=True):
    pos = nx.spring_layout(G)
    
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
    
    node_sizes = [v * 2000 for v in betweenness.values()]
    
    node_colors = [closeness[node] for node in G.nodes()]
    
    fig, ax = plt.subplots(figsize=(15, 15))
    if show_labels:
        nx.draw(
            G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, 
            cmap=plt.cm.viridis, edge_color='gray', font_size=8, ax=ax
        )
    else:
        nx.draw(
            G, pos, with_labels=False, node_size=50, node_color=node_colors, 
            cmap=plt.cm.viridis, edge_color='gray', ax=ax
        )
    plt.title("Соц. граф с центральностью посредничества и близости")
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
    sm.set_array(node_colors)
    fig.colorbar(sm, ax=ax, label="Центральность близости")
    plt.show()
    
    print("\nЦентральность посредничества:")
    sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    for name, centrality in sorted_betweenness[:10]:
        print(f"{name}: {centrality:.4f}")
    
    print("\nЦентральность близости:")
    sorted_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
    for name, centrality in sorted_closeness[:10]:
        print(f"{name}: {centrality:.4f}")
    
    print("\nСобственная центральность:")
    sorted_eigenvector = sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)
    for name, centrality in sorted_eigenvector[:10]:
        print(f"{name}: {centrality:.4f}")

def main():
    token = "" # воткнуть токен
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    user_id = "" # воткнуть айди друга для скана
    friends_data = getFriendsInfo(vk, user_id)

    G = createSocialGraph(friends_data)
    plotGraph(G, show_labels=False) # поменять если нужны имена

if __name__ == "__main__":
    main()
