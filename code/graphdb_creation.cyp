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



MATCH (c1:Customer)-[:MAKE]->(t1:Transaction)-[:WITH]->(m1:Merchant)
WITH c1, m1
MERGE (p1:Placeholder {id: m1.id})

MATCH (c1:Customer)-[:MAKE]->(t1:Transaction)-[:WITH]->(b1:Merchant)
WITH c1, b1, count(*) as cnt
MATCH (p1:Placeholder {id:c1.id})
WITH c1, b1, p1, cnt
MATCH (p2:Placeholder {id: b1.id})
WITH c1, b1, p1, p2, cnt
CREATE (p1)-[:Payes {cnt: cnt}]->(p2)

CALL algo.pageRank('Placeholder', 'Payes', {writeProperty: 'pagerank'})
