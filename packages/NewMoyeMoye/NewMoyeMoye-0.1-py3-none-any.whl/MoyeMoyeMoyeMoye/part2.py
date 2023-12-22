from py2neo import Graph, Node, Relationship

graph = Graph(password="abdulhadihub")

deleteQuery = "match(n) detach delete n"
graph.run(deleteQuery)

script = """
    create (hadi:Person {name: "hadi", marks: 96})
    create (zain:Person {name: "zain", marks: 96})
    create (ali:Person {name: "ali", marks: 90})
    create (faraz:Person {name: "faraz", marks: 100})
    create (farhan:Person {name: "farhan", marks: 90})
    create (hadi)-[:FRIENDS_WITH]->(faraz)
    create (hadi)-[:FRIENDS_WITH]->(zain)
    create (hadi)-[:FRIENDS_WITH]->(ali)
    create (hadi)-[:FRIENDS_WITH]->(farhan)
"""

query1 = """
match (faraz:Person {name: 'faraz'})
set faraz.marks = 0
return faraz.marks
"""

query2 = """ 
    match (farhan:Person)
    where farhan.name = "farhan"
    detach delete farhan
"""

query3 = """
    match (hadi:Person)
    where hadi.name = "hadi"
    merge (hadi)-[:FRIENDS_WITH]->(ayan:Person {name:"ayan"})
"""

graph.run(script)
graph.run(query1)
graph.run(query2)
graph.run(query3)

