# Sumerian-Social-Network-Project
<p>connect to database: in mysql shell do
	\connect external@sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com
with password:
	turamili
then do
	\use sumerianDB
to set default schema
then do
	\sql
to enter sql query mode

the external user has permissions to select from all tables in sumerianDB
</p>

# Packages
<p>networkx
plotly
dash-cytoscape
pandas
pydot
graphviz
</p>

# File Structure
``` 
|__ C++ --> Contains all the C++ scripts this project uses
	|__ DataCollection --> Code that mines/searches/and moves data
	|__ FamilyTree --> Contains all the code that is being used to construct family trees from the dataset
		|__ Data --> Contains code used to mine, sort, and filter data for the family tree
		|__ Tree --> Contains code used to construct the family tree based off the data in Data/
|__ Dataset --> Raw data that is being used
	|__ Output --> Script outputs that analyze data in the Dataset directory
        |__ Translated --> The data set run through the translation pipeline
	|__ TranslatedBasketTablets --> List of all basket tablets from Translated/
	|__ Untranslated --> Separated list of all untranslated tablets from ur_3untranslated.atf
	|__ UntranslatedBasketTablets --> List of all basket tablets from Untranslated/
        ur_3untranslated --> The complete raw data set
|__ ProjectDocuments --> Contains the Project documentation
|__ Python/ --> Contains all the python scripts this project uses
        |__ Core
                |__ Database --> Code that creates and queries the database
                |__ DataCollection --> Code that mines the raw data to be used in the database
        |__ Helpers --> Code snippets for automation of data formatting and other miscellaneous code
        |__ Temp --> Temporary Code that got pushed for some reason...
```
