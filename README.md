# Hallucinated Reference Checker

This application is intended to take references from an academic essay or a public research paper and check using scholarly sites if these references exist and are accurate or if they are ‘hallucinated’ – where references are AI-generated and inaccurate due to generative AI’s or LLMs’ lack of ability to process requests like this. It also handles formatting and returns the reference style a reference is written in.
The algorithm has been completed to a basic level, with areas of improvement in regards to the data it can handle and process, including improving accuracy, and additional verification of references.

**Steps on How to Use**

Coding file Steps on How to Use

Coding file **needs** to be in **same directory** as Word file containing references

1.	Run file and in the terminal, a prompt asking to enter the file name including the .docx extension will show up
2.	File is open and read and any info from ‘reference’ heading down will be taken line by line to extract references
3.	References then checked for reference style using regex. These are outputted alongside the reference parameters once ran through Scopus
4.	Scopus queries and delivers results – stating if it has been found or not
5.	If found, all search query fields are outputted

**Current Final Output**

<img width="498" height="194" alt="image" src="https://github.com/user-attachments/assets/3c31e257-93cd-4a73-be11-d54a57adaccc" />

**Libraries Used**

**re module** – regular expressions module used for reference stycle parser 

**requests module** – interacts with Elsevier API to fetch from API URL

**docx module and Document class** – opens and reads an imported Word doc

**Use of APIs**

The API used in this application is a Scopus Search API, accessed via API key through the Elsevier Developer Portal. This API was accessed through non-commercial for research purposes. This was chosen as many APIs were non-free to access or had limited uses per month if free- not optimal in this testing of my proposed algorithm.

The original aim of this application was a Google / Google Scholar-based API. However, there is no official one and this is not widely available through third partys.

Scopus as a searching website is limited as its primary focus is scientific journals, not accounting for books and web sources, amongst many. In my initial test case, a positive result is shown despite my main test case being a book reference. Upon manual searching, the reference **does not** exist in Scopus.

**Reference Style Parser**

The system begins with a reference parser, using regex patterns and dictionaries to compare a parsed reference to the Harvard and APA styles only, currently. The regex patterns can be improved upon to provide more accuracy but current is correct to a certain level. The regex patterns are broke down in the comments of the code file.
