# Hallucinated Reference Checker

This application is intended to take references from an academic essay or a public research paper and check using scholarly sites if these references exist and are accurate or if they are ‘hallucinated’ – where references are AI-generated and inaccurate due to generative AI’s or LLMs’ lack of ability to process requests like this. It also handles formatting and returns the reference style a reference is written in.
The algorithm has been completed to a basic level, with areas of improvement in regards to the data it can handle and process, including improving accuracy, and additional verification of references.

**Use of APIs**

The API used in this application is a Scopus Search API, accessed via API key through the Elsevier Developer Portal. This API was accessed through non-commercial for research purposes. This was chosen as many APIs were non-free to access or had limited uses per month if free- not optimal in this testing of my proposed algorithm.

The original aim of this application was a Google / Google Scholar-based API. However, there is no official one and this is not widely available through third partys.

Scopus as a searching website is limited as its primary focus is scientific journals, not accounting for books and web sources, amongst many. In my initial test case, a positive result is shown despite my main test case being a book reference. Upon manual searching, the reference **does not** exist in Scopus.



