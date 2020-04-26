CREATE CONSTRAINT ON (c:Customer) ASSERT c.id IS UNIQUE;
CREATE CONSTRAINT ON (m:Merchant) ASSERT m.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM
"file:///bs140513_032310.csv" AS line
WITH line,
SPLIT(line.customer, "'") AS customerID,
SPLIT(line.merchant, "'") AS merchantID,
SPLIT(line.age, "'") AS customerAge,
SPLIT(line.gender, "'") AS customerGender,
SPLIT(line.category, "'") AS transCategory

MERGE (customer:Customer {id: customerID[1], age: customerAge[1], gender: customerGender[1]})

MERGE (merchant:Merchant {id: merchantID[1]})

CREATE (transaction:Transaction {amount: line.amount, fraud: line.fraud, category: transCategory[1], step: line.step})-[:WITH]->(merchant)
CREATE (customer)-[:PERFORMS]->(transaction);



MATCH (c1:Customer)-[:PERFORMS]->(t1:Transaction)-[:WITH]->(m1:Merchant)
WITH c1, m1
MERGE (p1:Placeholder {id: m1.id})

MATCH (c1:Customer)-[:PERFORMS]->(t1:Transaction)-[:WITH]->(m1:Merchant)
WITH c1, m1, count(*) as cnt
MERGE (p2:Placeholder {id:c1.id})

MATCH (c1:Customer)-[:PERFORMS]->(t1:Transaction)-[:WITH]->(m1:Merchant)
WITH c1, m1, count(*) as cnt
MATCH (p1:Placeholder {id:m1.id})
WITH c1, m1, p1, cnt
MATCH (p2:Placeholder {id: c1.id})
WITH c1, m1, p1, p2, cnt
CREATE (p2)-[:PAYS {cnt: cnt}]->(p1)

MATCH (c1:Customer)-[:PERFORMS]->(t1:Transaction)-[:WITH]->(m1:Merchant)
WITH c1, m1, count(*) as cnt
MATCH (p1:Placeholder {id:c1.id})
WITH c1, m1, p1, cnt
MATCH (p2:Placeholder {id: m1.id})
WITH c1, m1, p1, p2, cnt
CREATE (p1)-[:PAYS {cnt: cnt}]->(p2)


// Computing PageRank for placeholder nodes
CALL algo.pageRank('Placeholder', 'PAYS', {writeProperty: 'pagerank'})

// Viewing the PageRank results
MATCH (p:Placeholder)
RETURN p.id AS id, p.pagerank as pagerank
ORDER BY pagerank DESC

CALL algo.pageRank.stream('Placeholder', 'PAYS', {
  iterations:20, dampingFactor:0.85, writeProperty: 'pagerank'
})
YIELD nodeId, score

// Computing the degree of each node
MATCH (p:Placeholder)
SET p.degree = apoc.node.degree(p, 'PAYS')

// Community detection using label propagation
CALL algo.beta.labelPropagation('Placeholder', 'PAYS', {write:true, writeProperty: "community", weightProperty: "cnt"})


MATCH (p:Placeholder)
RETURN p.id AS id, p.pagerank as pagerank, p.degree as degree, p.community as community

// Computing node similarity
CALL algo.nodeSimilarity('Placeholder', 'PAYS', {writeProperty: 'similarity'})

// Query to obtain the relationships of a particular customer node
match (c1:Customer)-[:PERFORMS]->(t1:Transaction)-[:WITH]->(m1:Merchant)
where c1.id = "C2054744914"
return c1, t1, m1
