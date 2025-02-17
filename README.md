<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Linguistic Qualtiy Detection of APIs</h3>

  <p align="center">
    SE+AI Research Lab, FCS, University of New Brunswick
    <br />
    <a href=""><strong>Explore the project »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://ieeexplore.ieee.org/abstract/document/10838121">CASCON Article</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

**Background:** APIs or Application Programming Interfaces help distributed systems and microservices to expose their functionalities and serve as a means for communication among them. Understandability and readability of APIs are important for effectively comprehending and using APIs. Despite the presence of established API design rules and guidelines (or design patterns), poor design practices (or antipatterns) are still prevalent in APIs. APIs with high-quality design are essential both for API providers and client developers. 

**Goal:** This paper aims to (1) assess the linguistic design quality of APIs in distributed systems and microservices by automatically detecting antipatterns and design patterns in APIs and (2) evaluate the impact of linguistic patterns and antipatterns on the understandability and readability of APIs. 

**Method:** We rely on syntactic and semantic analyses for automatic assessment of the design quality of APIs using detection heuristics. Syntactic analysis involves analyzing the structure and syntax of the APIs, while semantic analysis involves analyzing API documentation, descriptions, and parameters. We also conduct a survey and ask participants to answer the purpose of the API snippets (comprehension task) and rate the difficulty in understandability and readability of the API snippets. 

**Findings:** We achieved an average accuracy of more than 94\% in detecting patterns and antipatterns. Our detection results also suggest that antipatterns are prevalent in the APIs of distributed systems and microservices. The findings of our survey revealed adherence to linguistic patterns significantly enhances the understandability and readability of APIs. In contrast, linguistic antipatterns have negative effects on the understandability and readability of Web APIs. 

**Conclusion:** Our findings will assist API developers in identifying poor design practices and improving the design quality of their APIs. Findings from our survey also highlight the importance of adhering to good API design practices to enhance the understandability and readability of APIs.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Methodology

![overall-method](/Journal-Resources/Images/overall-method.jpg)

<!-- Patterns and Anti-Patterns -->
## Linguistic Patterns
Linguistic patterns and antipatterns studied in this are availabele <a href="/Journal-Resources/Detection-Heuristics/Linguistic-patterns-antiopatterns.pdf"> here </a>. Additionally, the detailed detection reuslt, analysis, and findings can be accessed <a href="/Journal-Resources/Detection/"> here </a>.


![detction-method](/Journal-Resources/Images/Detection/detection-method.jpg)



## Impact Survey
The impact survey, which assesses the effects of linguistic patterns and antipatterns on API understandability and readability, is available for review <a href="/Journal-Resources/Impact-Survey/Impact-Survey-Design.pdf"> here </a>. Additionally, the collected survey data and detailed analysis, including statistical insights and findings, can be accessed <a href="/Journal-Resources/Impact-Survey/"> here </a>.


![impact-study-method](/Journal-Resources/Images/Impact/impact-study.jpg)





### Built With



* Python
* WorNet
* LDA Topic Model
* NLTK
* SPacy
* SPacy Similarity (Cosine)
* Inflect

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.



### Prerequisites
1. <a href="https://www.python.org/downloads/"> Python </a> 3.6 or higher
2. <a href="https://www.r-project.org/"> R </a> and <a href="https://posit.co/download/rstudio-desktop/"> R Studio </a>

### Installation

1. Clone the repo
   ```sh
   git clone [url] 
   ```
2. Downloads
   ```sh
   npm install [url]
   ```
3. Install all the libraires
   ```sh
   pip install nltk
   pip install spacy
   pip install gensim
   pip install inflect
   pip install sklearn
   ```
4. Required downloads
   ```sh
   nltk.download('wordnet')
   nltk.download('stopwords')
   nltk.download('punkt')
   nltk.download('omw-1.4')
5. Run the python script
   ```sh
   python3 test.py
   python run_all.py
   ```
6. Run the R script
   ```sh
   survey-analysis.R
   ```
  


### File Structure


```
API-Quality/
├── REST/
│   ├── APIs
│   │   ├── API_Name.txt
├── GraphQL/
│   ├── APIs
│   │   ├── API_Name.txt
├── All-Data/
│   ├── output_data.jsonl
│   ├── result_summary.csv
├── Journal Resources/
│   ├── Images/
│   │   ├── Detection/
│   │       ├── {image}.pdf
│   │   ├── Impact/
│   │       ├── {image}.pdf
│   ├── Detection-Result/
│   │    ├── Validation Result.xlsx
│   │    ├── RQ Analysis.xlsx
│   │    ├── result_summary.csv
│   ├── Impact-Survey/
│   │    ├── results-survey.csv
│   │    ├── survey-analysis.R
│   │    ├── Impact-Survey-Design.pdf
│   │    ├── patterns.yaml
│   │    ├── antipatterns.yaml
│   │    ├── data-cleaning-protocol.md
│   │    ├── dataset-description.md
│   ├── api_analyzer.py
│   ├── data-count.py
│   ├── display_options.py
│   ├── file_handler.py
│   ├── result_summary.py
│   ├── run-all.py
│   ├── test.py
│   ├── uri_cleaning.py
│   ├── acronyms.txt
```





<!-- LICENSE -->
## License and Copyright
Copyright (c) 2025 [SE+AI Lab]

Permission is granted to use, copy, modify, and distribute this project with credit to SE+AI Lab.

THE PROJECT IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.





<!-- CONTACT -->
## Contact

[SE+AI Lab](https://seai-researchlab.github.io/)
<p align="right">(<a href="#readme-top">back to top</a>)</p>






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
