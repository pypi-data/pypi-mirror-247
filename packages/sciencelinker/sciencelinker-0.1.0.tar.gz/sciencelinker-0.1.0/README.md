# ScienceLinker: Enriching survey data with data from knowledgebases – and more



## Abstract
Data enrichment is a central part in many research proposals and daily work of data analysts. 
Merging multiple datasets especially from different domains allows for new analyses and research insights. 
Hereby enrichment is achieved by interlinking corresponding data items of two datasets and adding the additional data from the second dataset to the first.
While the general procedure tends to be recurrent, in practice further challenges arise.
Most of the time researchers require fully transparent and documented workflows where each step e.g. identification of compatible item types or of comparison keys can be inspected and fully controlled. 
However, understanding and accessing new knowledge bases requires time and can be cumbersome.
Adding that sufficiency of data quality of less known datasets needs to be assessed yet.
Sciencelinker is a toolset that aggregates functionality to enrich primarily social science survey data but also other datasets.
The ScienceLinker python module integrates seamlessly with your data analysis setup and gives you full control of your analyses.
It allows for data linking and enrichment with large established KBs like DBpedia, WikiData, GeoNames, or other LOD knowledge bases.
Furthermore, the module provides the means to design a step-by-step transparent enrichment workflow using methods ranging from linking via direct field comparisons up to text analysis for more complex scenarios.
Additionally, it supports the retrieval of Twitter microposts, to allocate complementing material for investigation. This includes speedy identification of relevant microposts for a given topic and first analysis steps, like filtering by language or location.

## Explorative Approach
At ScienceLinker, users from diverse domains with computational expertise find a welcoming gateway to the world of data linking, 
even if they are initially unaware or skeptical of such methods and data sources. Our platform showcases a powerful and versatile 
set of tools, enabling users to analyze data comprehensively and extract various types of information, forming the essential foundation 
for successful data linking endeavors. By combining complementary methods, ScienceLinker offers users the opportunity to swiftly explore 
new methods and integrate multiple data sources, gaining insights into potential benefits for their own work, despite the outcomes not always 
being perfect. With our all-in-on Python package, well-documented processes, and detailed processing logs, users can confidently navigate the 
intricacies of data linking.




## ScienceLinker Overview
ScienceLinker is optimized for survey data but our methods can be applied on various kinds of data.
1.	Tabular data: Data that is or can be structured in a table, this includes linked data. Rows or columns are used as input and can contain short texts or numbers. This data is eligible for linking with KB resources by comparing the values of denominated columns with property values of the resources. Also, identifying of compatible resource types can be supported.
2.	Textual data: Longer texts that are part of research data, e.g. free text answers of respondents or comments in web forums etc. Named Entity Recognition and topic modelling can be used to analyse larger datasets automatically in a structured and fast way.
3.	Content data: A keyword defining a topic of interest especially a social science concept can be used to compile a set of microposts that serves a additional material for investigation.

<div align="center">
<img src="http://sciencelinker.git.gesis.org/docs/_images/functions_overview.jpg" width="500"/>
</div>

## Documentation
Please find the documentation to our package and methods at [http://sciencelinker.git.gesis.org/docs/](http://sciencelinker.git.gesis.org/docs/index.html).

## SPARQL Lookup in Knowledge Graphs
KGs are a source for additional information that can be used to enrich a local dataset. A possible scenario: Given a list of 
country names or codes from survey data, ScienceLinker can be used find resources in a KG that are of a given type (eg. country) 
and have a label that matches with a country name from the given list. Such resources bear additional information such as 
“Population density”, “Area” or “GNP” that can enrich the local dataset. [More](http://sciencelinker.git.gesis.org/docs/kg_coverpage.html)

## Geonames Lookup
ScienceLinker incorporates the functionality to retrieve longitude and latitude information for a given set of location names, 
such as cities and countries, by utilizing the GeoNames web services. 
This feature proves valuable in computing proximities between places, facilitating linking operations and enabling further 
analyses based on geographical relationships. [More](http://sciencelinker.git.gesis.org/docs/geo_names.html)


## Named Entity Recognition (NER)
The integration of NER within ScienceLinker enables the extraction of structured information from unstructured text. By utilizing 
the DBpedia URLs associated with recognized entities, it becomes possible to establish links to additional data within the DBpedia Knowledge Graph, 
enhancing the given dataset that contains text. [More](http://sciencelinker.git.gesis.org/docs/ner_dbpspot.html)

## Topic Modelling
Topic modelling is a valuable technique used to extract topics from a collection of documents. It involves representing topics as 
sets of words, utilizing the co-occurrence probabilities of words within the document set. One popular method for topic modelling 
is [Latent Dirichlet Allocation (LDA)](https://papers.neurips.cc/paper/2010/file/71f6278d140af599e06ad9bf1ba03cb0-Paper.pdf).

The application of LDA within ScienceLinker enables the analysis of longer texts, such as online discussions, chats, articles, 
and various other forms of written content. By identifying the topics present in a document, it becomes possible to establish 
connections between documents that share similar topics. [More](http://sciencelinker.git.gesis.org/docs/lda_gensim.html)

## Micropost retrieval
Online discourse contains latent information about the attitudes and opinions of individuals on current and past topics, expressed 
in a more natural context than traditional surveys. Analyzing online discourse provides an opportunity to gain additional insights into 
respondents’ behavior, complementing findings from conventional surveys. Simultaneously, it enables the examination of the attitudes of 
a diverse range of social media users towards specific subjects.

These valuable insights can be extracted using Natural Language Processing techniques, such as sentiment analysis and stance detection, 
from the discourse. However, the user faces several challenges before that. [More](http://sciencelinker.git.gesis.org/docs/mpr_coverpage.html)

## Contact
* Dr. Benjamin Zapilko: benjamin.zapilko@gesis.org
* Felix Bensmann: felix.bensmann@gesis.org

## Funding
This project is funded by the Deutsche Forschungsgemeinschaft (DFG) under the Grant No. [404417453](https://gepris.dfg.de/gepris/projekt/404417453).


## Third Party Efforts
Our software project is built upon the collaborative efforts of various third-party resources, including libraries, web services, and data sources. 
We rely on the invaluable contributions of [DBpedia Spotlight](https://www.dbpedia-spotlight.org/), [GeoNames](https://www.geonames.org/about.html), 
and [Gensim](https://radimrehurek.com/gensim/), which generously provide their offerings free of charge, only requesting proper attribution, a 
condition we are delighted to honor. Moreover, we extend our gratitude to the multitude of projects, akin to [DBpedia](https://www.dbpedia.org/) 
and [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), for their unwavering commitment to sharing data freely on the 
semantic web. While we wholeheartedly embrace these open resources, it is essential to acknowledge that each data provider may have individual 
terms and conditions governing the use of their data, and we encourage our users to adhere to these guidelines with respect and appreciation 
for the valuable data made accessible to us.

