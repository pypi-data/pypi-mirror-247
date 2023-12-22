from py2neo import Graph, Node, Relationship

graph = Graph(password="12345678")

# Create nodes or merge if they exist
c = graph.run("MERGE (p:person {name: 'Bob'}) RETURN p").evaluate()
d = graph.run("MERGE (p:person {name: 'Alice'}) RETURN p").evaluate()

# Create animal nodes
node1 = Node("animal", name="tommy")
node2 = Node("animal", name="jerry")
graph.create(node1)
graph.create(node2)

# Create relationships
graph.run(f"MATCH (p:person {{name: 'Bob'}}), (a:animal {{name: 'tommy'}}) CREATE (p)-[:HAS_PET]->(a)").evaluate()
graph.run(f"MATCH (p:person {{name: 'Alice'}}), (a:animal {{name: 'jerry'}}) CREATE (p)-[:HAS_PET]->(a)").evaluate()