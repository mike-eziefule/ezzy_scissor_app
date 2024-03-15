<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Logo -->
<br />
<div align="center">
  <a href="https://github.com/mike-eziefule/ezzy_scissor_app">
    <img src="./static/images/misc/EZZY-SCISSOR.gif" alt="Logo" width="80%" height="20%">
  </a>
</div>

<br/>

<div>
  <p align="center">
    <a href="https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.loom.com/share/ed3cc4bfb8c743cd9371e2831a7785ec?sid=4be6af19-e752-4289-a180-bf065c0bd58a">View Demo</a>
    ·
    <a href="https://github.com/mike-eziefule/ezzy_scissor_app/issues">Report Bug</a>
    ·
    <a href="https://github.com/mike-eziefule/ezzy_scissor_app/issues">Request Feature</a>
  </p>
</div
---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-Ezzy-scissor">About Ezzy Scissor</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#lessons-learned">Lessons Learned</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Blog. -->
## About Ezzy Scissor app

Ezzy scissor is fully function URL Shortener API, that is simple to use, and long URLs can become short and manageable with just a few clicks. 

With Ezzy_scissors, users can personalize your shortened URLs to align with your brand identity. Utilize custom slugs, branded links, and domain customization options to reinforce your brand presence and enhance user engagement. Also, a free QRCode is available, customized to carry your unique URL links.

Users are encouraged to register using the registration form, here basic details such as First Name, Last Name, email and password would be required. After registration, A personalized dashboard containing all the users activities woulb be created and users will be able to access it by logging in with their email and password.

All long URLs will be saved, giving the client the opportunity to customize, generate qrcode or delete when necessary.

Analyses, such as date created and number of clicks information will be available in the dashboard.

Rate limiting has also been to 3 repetition per minute. To manage the health of the API, Users will be able to logged out automatically if a perticilar route is used more than three times with a minute.

Ezzy scissor was built as a Capstone project by <a href="https://github.com/mike-eziefule/">Eziefule Michael</a>, a Backend Engineering student at <a href="https://engineering.altschoolafrica.com/">AltSchool Africa</a> who's learning to create magic with the Python FastAPI framework.

A tutorial on how this project was built is available  soon on [Michael_Ezzy's Space](https://hashnode.com/draft/6539339dbe20a1000f0b5edd) on Hashnode.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![FastAPI][fastapi]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project. -->
## Lessons Learned

Creating this blog helped me learn and practice:
* The use of python for backend development
* Debugging
* Routing
* Database Management
* Internet Security
* User Authentication
* User Authorization
* Website Deployment
* Rate Limiting
* Documentation

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Usage

To get a local copy up and running, follow the steps below.

### Prerequisites

Python3: [Get Python](https://www.python.org/downloads/)

### Installation

1. Clone this repo
   ```sh
   git clone https://github.com/mike-eziefule/ezzy_scissor_app.git
   ```
2. Activate the virtual environment
   ```sh
   source env/Scripts/activate
   ```
3. Install project packages
   ```sh
   pip install -r requirements.txt
   ```
4. Run uvicorn
   ```sh
   uvicorn main:app --reload
   ```
5. Open the link generated in the terminal on a browser  
   ```sh
   http://127.0.0.1:8000
   ```

### Alternatively
1. This App has been hosted at onrender.com To test, follow the link below.

   ```sh
   https://ez-ly.onrender.com
   ```

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br />

[![Ezzy scissor Landing page][landing_page]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/landing_page.png)
[![Ezzy scissor Login page][login]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/login.png)

[![Ezzy scissor Register page][register]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/register.png)

[![Ezzy scissor Dashboard page][dashboard1]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/dashboard1.png)

[![Ezzy scissor Dashboard2 page][dashboard2]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/dashboard2.png)

[![Ezzy scissor Create new page][createnew]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/createnew.png)

[![Ezzy scissor Customize page][customize_url]](https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/static/images/misc/customize_url.png)



<br/>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

X [Formally Twitter] - [@EziefuleMichael](https://twitter.com/EziefuleMichael)

Project Link: [Ezzy_Scissor](https://github.com/mike-eziefule/Ezzy_Blog_api)

Email Address: [mike.eziefule@gmail.com](mailto:mike-eziefule@gmail.com)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's FastAPI Lessons](https://github.com/CalebEmelike)
* [W3School html tutorial](https://w3schools.com)
* [GitHub Student Pack](https://education.github.com/globalcampus/student)
* [Canva](https://www.canva.com/)
* [Stack Overflow](https://stackoverflow.com/)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/mike-eziefule/ezzy_scissor_app
[contributors-url]: https://github.com/mike-eziefule/ezzy_scissor_app/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mike-eziefule/ezzy_scissor_app
[forks-url]: https://github.com/mike-eziefule/ezzy_scissor_app/network/members
[stars-shield]: https://img.shields.io/github/stars/mike-eziefule/ezzy_scissor_app
[stars-url]: https://github.com/mike-eziefule/ezzy_scissor_app/stargazers
[issues-shield]: https://img.shields.io/github/issues/mike-eziefule/ezzy_scissor_app
[issues-url]: https://github.com/mike-eziefule/ezzy_scissor_app/issues
[license-shield]: https://img.shields.io/github/license/mike-eziefule/ezzy_scissor_app
[license-url]: https://github.com/mike-eziefule/ezzy_scissor_app/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/twitter/follow/EziefuleMichael
[twitter-url]: https://twitter.com/EziefuleMichael
[landing_page]:static/images/misc/landing_page.png
[login]:static/images/misc/landing_page.png
[register]:static/images/misc/register.png
[dashboard1]:static/images/misc/dashboard1.png
[dashboard2]:static/images/misc/dashboard2.png
[createnew]:static/images/misc/createnew.png
[customize_url]:static/images/misc/customize_url.png

[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[fastapi]: https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=black
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white