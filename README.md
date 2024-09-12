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
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Linguistic Qualtiy Detection of APIs</h3>

  <p align="center">
    SE+AI Research Lab, FCS, University of New Brunswick
    <br />
    <a href=""><strong>Explore the project »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Data Sets</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Articles</a>
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

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Application Programming Interfaces (APIs) define how Web services, middle-wares, frameworks, and libraries communicate with their clients. An API that conforms to REpresentational State Transfer (REST) design principles is known as REST API. At present, it is an industry-standard for interaction among Web services. An API that conforms to the REST design principles would arguably be easier to use and understand, would create less frustration for application developers, and more widespread use of API . To assess the linguistic design quality of REST APIs, researchers defined linguistic patterns (i.e., best practices of REST API design) and linguistic antipatterns (i.e., poor REST API design practices to avoid). REST APIs that follow linguistic patterns are easier to understand and use. In contrast, linguistic antipatterns hinder the understanding and use of REST APIs. High linguistic design quality would, logically, be more important for public and partner APIs compared to private APIs as public and partner APIs are intended for use outside of the developing organization.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Patterns and Anti-Patterns -->
## Common Patterns and Anti-Pattens in API Design

* **Tidy vs. Amorphous End-point:** End-points in REST should be tidy and easy to read. A Tidy End-point has an appropriate lower-case resource naming, no extensions, underscores, or trailing slashes. Amorphous End-point occurs when an end-point contains symbols or capital letters that make them difficult to read and use. An end-point is amorphous if it contains: (1) upper-case letter, (2) file extensions, (3) underscores, and, (4) a final trailing-slash. For example: The end-point /NEWCustomer/image01.tiff/ is an Amorphous End-point while the end-point /customers/1234 is a Tidy End-point.

* **Contextualized vs. Contextless:** Resource names in End-points should be contextual, i.e., nodes in end-points should be semantically-related. Contextless Resource Names antipattern appears when endpoints are composed of nodes that do not belong to the same semantic context. In contrast, if the nodes in an end-point belong to same semantic context this is known as Contextual Resource Names pattern. For example: The endpoint /newspapers/planet/players?id=123 is Contextless Resource while the end-point /soccer/team/ players?id=123 is Contextual Resource. 

* **Verbless vs. CRUDy Endpoint:** Appropriate HTTP methods, e.g., GET, POST, PUT, or DELETE, should be used to perform an action. The use of CRUDy terms (e.g., create, read, update, delete, or their synonyms) as part of the end-point design is inappropriate and known as CRUDy Endpoint. In contrast, an endpoint without any CRUDy term in its resource name is known as Verbless End-point pattern. For example: The endpoint /update/players/age?id=123 is a CRUDy Endpoint while the end-point /players/age?id=123 is a Verbless End-point. 

* **Consistent vs. Inconsistent Documentation:** The Inconsistent Documentation antipattern occurs when an endpoint (together with the HTTP method) is in contradiction with its documentation. When the endpoint and HTTP method aligns with its documentation, this is known as Consistent Documentation pattern. For example: The POST method with the endpoint /bulk/devices/ remove is in contradiction with its documentation 'Delete multiple devices. Delete multiple devices, each request can contain a maximum of 512kB', thus, is an Inconsistent Documentation. In contranst, the endpoint /bulk/devices/remove with the documentation 'Remove multiple devices. Remove multiple devices, each request can contain a maximum of 512kB', would be identified as Consistent Documentation. 

* **Standard vs. Non-standard Endpoint:** An Endpoint design should not include resources with non-standard identification, which hinders the reusability and understandability of APIs. Non-standard Endpoint Antipattern occurs when (1) characters like ´e, ˚a, ¨o, etc. (2) blank spaces , (3) double hyphens, and (4) unknown characters (e.g., !, @, #, $, %, ˆ, &, *, etc.) are present in endpoints. In contrast, an standard endpoint non-standard characters. For example: The end-point /museum/louvre/r´eception/ is an example of Non-standard URI Design. While, the end-point /museum/louvre/reception/ represents Standard endpoint Design. 

* **Pertinent vs. Non-pertinent Documentation:** The Non-pertinent Documentation antipattern occurs when the documentation of an endpoint is not cohesive to the design of the endpoint itself. In contrast, a well-documented endpoint clearly describe its purpose using semantically related terms can be considered as Pertinent Documentation pattern . For example: The endpoint and documentation pair from Twitter: api.twitter.com/1.1/favorites/list – ‘Returns the 20 most recent Tweets liked by the authenticating or specified user’ is considered as a Non-pertinent Documentation. In contrast, this endpoint and documentation pair from Instagram: instagram.com/ media/media-id/comments – ‘Gets a list of recent comments on a media object. The public content permission scope is required to get comments for a media that does not belong to the owner of the access token.’ is considered as a Pertinent Documentation. 

* **Hierarchical vs. Non-hierarchical Nodes:** Nodes in an endpoint should be hierarchically related to its neighbor nodes. Non-hierarchical Nodes is an antipattern that appears when at least one node in an endpoint is not hierarchically related to its neighbor nodes. When all the nodes in an end-point are in a hierarchical relationship, this is known as Hierarchical Nodes pattern. For example: The end-point /professors/faculty/university is an example of Non-hierarchical Nodes while the end-point /university/faculty/professors is an example of Hierarchical Nodes. 

* **Singularized vs. Pluralized Nodes:** Endpoints should use singular/plural nouns consistently for resources naming. When clients send PUT or DELETE requests, the last node of the request endpoint should be singular. In contrast, for POST requests, the last node should be plural. Therefore, the Pluralized Nodes antipattern appears when plural names are used for PUT/DELETE requests or singular names are used for POST requests, otherwise it can be considered as Singularized Nodes pattern . For example: The POST method with the endpoint /team/player is a Pluralized Nodes while the POST method with the endpoint /team/players is a Singularized Nodes. 

* **Self-descriptive vs. Non-descriptive End-point:** Endpoints should be short and precise, i.e., as few characters as possible while still maintaining usability. Non-descriptive endpoint antipattern occurs when the endpoint design has encoded nodes, e.g., simple resource names not used, which hinder its understandability. In contrast, a Self-descriptive End-point has clear and concise resource identifiers. For example: The end-point /auth/token/from oauth is a Nondescriptive while the end-point /account/set profile photo is a Self-descriptive.

* **Non-Filerting-URI vs Filerting Endpoints:** 
Endpoints should always incorporate SPF (Sorting, Pagination, and Filtering) factors. Users often try to fetch large amounts of data, and SPF helps limit the number of collections that can be retrieved from a list of resources. Further, SPF allows API consumers to filter collections according to their needs. This reduces data loading time, makes responses easier to handle, and reduces network traffic. An endpoint that incorporates SPF factors is known as a Filtering-Endpoint pattern, while an endpoint that does not incorporate SPF factors is known as a Non-Filtering-Endpoint antipattern.

Pattern: (from Cisco Flare)
/environments?latitude={latitude}&longitude={longitude} Gets a list of all environments. Params can include the following: If latitude and longitude are specified, gets a list of environments whose geofence contains the given point. The geofence of each environment includes all points within a particular distance from a point on earth.

/environments?key={key}&value={value} Gets a list of all environments. Params can include the following: If key and value are specified, returns environments whose data objects contain the given key/value pair.

Anti-pattern:
/environments List environments. Gets a list of all environments.

* **Parameter Tunneling vs  Parameter Adherence**


Web APIs often have path parameters and query parameters to file specific resources. Path parameters (e.g., /api/books/{id})  are used to identify or retrieve a specific resource, while query parameters (e.g., /api/books?category=fiction) are used for sorting, filtering, and pagination of the request data. Path parameters should be used to identify resources (e.g. delete, update, create, etc). In contrast, query parameters should be used for sorting, filtering, and pagination of resources. Parameter Tunneling antipattern occurs if path parameters are used for sorting, filtering, and pagination, or query parameters are used for identifying resources. Consistent use of path and query parameters would result in a Parameter Adherence pattern.

Pattern:
/desserts?type=cake&seller-id=1234   Return all the resource types cakes with seller-id of 11234 
/v1/me/ratings/albums/{id}    Remove a user’s album rating by using the album’s identifier.

Anti-Pattern:
/desserts?page=5&pageSize=25 Update the resource desserts

* **Consistent Resource Archetype Names vs Inconsistent Resource Archetype Names**

Resource archetypes are the basic building blocks of API endpoints. Two of the most commonly used resource archetypes are Document and Collection. The Document archetype usually includes fields filled with values that describe a resource, while a Collection resource is a list of document resources. To maintain clarity, singular nouns should be used for naming Documents, while plural nouns should be used for naming Collections. Adhering to these rules results in the Consistent Resource Archetype Names pattern. In contrast, the Inconsistent Resource Archetype Names antipattern occurs if plural nouns are used for naming documents or singular nouns are used for naming collections.

Pattern:
GET /recipes/desserts/apple-pie

Anti-Pattern: 
GET /recipe/dessert/apple-pies

* **Identifier Annotation vs Identifier Ambiguity**

Path parameters or resource identifiers used in endpoints should be enclosed in curly braces, angle brackets, or followed by a colon sign. Using such symbols in endpoint design is referred to as Identifier Annotation pattern, which improves endpoint readability and understandability. In contrast, the absence of curly braces, angle brackets, or colon to represent resource identifiers would result in an Identifier Ambiguity antipattern.

Pattern:
/v2/lists/:id/members
/appInstallation/{id}
/rules/<ruleID>

Anti-Pattern:
/rules/ruleKey
/idFromLegacyId


* **Flat vs Structured Endpoint**

Forward slash (/) must be used to separate nodes of an endpoint and indicate a hierarchical relationship. A structured Endpoint pattern occurs when forward slashes are used to break down complex resource names to improve the readability and understandability of the endpoint. In contrast, a Flat Endpoint antipattern occurs when complex or large resource names are not broken down with forward slashes.

Pattern: 
/requests/{request_id}/receipt
/requests/{request_id}/map

Anti-Pattern:
/requestFirmwareUpdateFromInStoreReader
/requestItemDisplayFromInStoreReader



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With



* Python
* WorNet
* LDA Topic Model
* NLTK
* SPacy
* SPacy Similarity (Cosie)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.





### Prerequisites and Installation




1. Clone the repo
   ```sh
   pip install 
   ```
2. Downloads
   ```sh
   npm install
   ```

 

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@krishnodey_](https://twitter.com/krishnodey_) -dey.krishno25@egmail.com
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
