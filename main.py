from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Define the Wikidata SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Add a User-Agent header
sparql.addCustomHttpHeader("User-Agent", "MythologyMachine/1.0 (https://github.com/compn/MythologyMachine)")

# SPARQL Query: Fetch mythological figures, their domains, and associated cultures
query = """
SELECT ?entity ?entityLabel ?cultureLabel ?domainLabel WHERE {
  ?entity wdt:P31 wd:Q22988604.  # Instance of a mythological figure
  OPTIONAL { ?entity wdt:P1408 ?culture. }  # Associated culture
  OPTIONAL { ?entity wdt:P101 ?domain. }  # Domain (e.g., war, wisdom)
  
  # Request labels in English
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} LIMIT 50
"""

# Set query and return format
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Execute query and parse results
results = sparql.query().convert()
data = []

# Extract results
for result in results["results"]["bindings"]:
    entity = result["entityLabel"]["value"] if "entityLabel" in result else "Unknown"
    culture = result["cultureLabel"]["value"] if "cultureLabel" in result else "Unknown"
    domain = result["domainLabel"]["value"] if "domainLabel" in result else "Unknown"
    data.append([entity, culture, domain])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Mythological Figure", "Culture", "Domain"])

# Display results
print("Mythology Data Query")
print(df)
