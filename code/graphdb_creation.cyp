LOAD CSV WITH HEADERS FROM
"file:///bs140513_032310.csv" AS line
RETURN line,
SPLIT(line.customer, "‘") AS customer_ID,
SPLIT(line.merchant, "‘") AS merchant_ID,
SPLIT(line.age, "‘") AS customer_age,
SPLIT(line.gender, "‘") AS customer_gender,
SPLIT(line.category, "‘") AS transaction_category
LIMIT 10
