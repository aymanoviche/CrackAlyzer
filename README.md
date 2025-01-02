<br />
<div align="center" id="readme-top">
  <a href="https://github.com/OussamaFannouch/CrackAlyzer">
    <img src="https://raw.githubusercontent.com/OussamaFannouch/CrackAlyzer/refs/heads/main/frontend/media/upper_ic.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">CrackAlyzer</h3>

  <p align="center">
    A secure and modular platform to analyze password strength, and Crack passwords, and check if your password has been leaked, built with FastAPI, ReactJS, and MongoDB for robust performance and scalability!    <br />
    <a href="https://oussamafannouch.me/CrackAlyzer">View Demo</a>
    ·
    <a href="https://github.com/OussamaFannouch/CrackAlyzer/issues/new">Report Bug</a>
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
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<img src="https://i.imgur.com/HthsLOX.png" alt="Logo" width="" height="">
<img src="https://i.imgur.com/5BfLcpd.png" alt="Logo" width="" height="">
<img src="https://imgur.com/6yrTA6T.png" alt="Logo" width="" height="">
<img src="https://imgur.com/6jwnw8y.png" alt="Logo" width="" height="">



This project is a comprehensive full-stack application designed to enhance password security. It offers powerful features such as:

-   **Secure User Authentication**: Includes signup, login, password hashing, and JWT-based session management for robust security.
-   **Password Strength Analyzer**: Assesses password strength based on complexity, length, entropy, and other factors.
-   **Password Breach Checker**: Identifies whether a password has been exposed in known data breaches.
-   **Password Cracker**: Attempts to crack provided password hashes and retrieve the plaintext password.
-   **Intuitive Frontend**: Built with ReactJS to deliver a smooth and user-friendly experience.

This platform is designed to promote better password practices, helping users safeguard their accounts with strong, secure passwords.



### Built With

* ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
* [![React][React.js]][React-url]
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.
### Prerequisites
Before you begin, ensure you have the following installed on your system:

-   **Python 3.10+**
-   **Node.js and npm**
-   **Docker (optional, for containerized deployment)**
-   **MongoDB (or you can use atlas MongoDB )**

### Installation


### Getting Started

To get a local copy up and running, follow these steps.

----------

#### Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.10+**
-   **Node.js and npm**
-   **Docker (optional, for containerized deployment)**
-   **MongoDB**

----------

#### Installation

1.  **Clone the repository**
    
    ```bash
    git clone https://github.com/OussamaFannouch/CrackAlyzer.git
    cd CrackAlyzer
    ```
    
2.  **Backend Setup**    
    -   Activate the virtual environment:
        
        ```bash
        python -m venv env
        source env/bin/activate  # For Linux/macOS
        .\env\Scripts\activate  # For Windows
        ```
        
    -   Install dependencies:
        
        ```bash
        pip install -r requirements.txt
        
        ```
        
    -   Configure environment variables in the `backend\auth_service\.env` file.
    -   Run the backend server (on the main folder run the following command):
        
        ```bash
        uvicorn backend.main:app --reload
        ```
        
3.  **Frontend Setup**
    
    -   Navigate to the frontend directory:
        
        ```bash
        cd frontend
        ```
        
    -   Install dependencies:
        
        ```bash
        npm install
        
        ```
        
    -   Start the frontend development server:
        
        ```bash
        npm run dev
        ```
        
4.  **Database Setup**
    
    -   Make sure MongoDB is running locally or configure it in the backend `.env` file. (or you can use atlas MongoDB)
    -   Create the necessary collections and indexes using the backend. (we have just one collection which called users)

----------
<!-- USAGE EXAMPLES -->
## Usage


-   Access the frontend at `http://localhost:3000`.
-   The backend API will run at `http://localhost:8000`.
-   Use the `/docs` endpoint (Swagger) for exploring the API.

Now you’re ready to explore the platform!



## Project Overview
<h3> File Structure:</h3>
<img src="https://imgur.com/aBX2f1o.png">
<h3> Authentification: </h3>
<img src= "https://imgur.com/pGjzuGX.png">
<h3> Password Analyzer : </h3>
soon....
<h3> Password Cracker : </h3>
soon....
<h3>Password Breach Checker :</h3>
soon....

<!-- ROADMAP -->
## Roadmap

- [x] -   **User Authentication**: Implement secure signup, login, and JWT-based session management.
- [x] -   **Password Analyzer**: Evaluate password strength based on complexity, entropy, and length.
- [x] -   **Responsive Frontend**: Ensure the React frontend is fully responsive across devices.
- [x] -   **Password Breach Checker**: Add functionality to check for known password breaches.
- [x] -   **Dashboard With History**: Develop a superuser dashboard for user management and monitoring.
- [ ] -   **Password Cracker**: Provide a hash-based password cracking feature for security testing.
- [ ] -   **Email Verification**: Implement email verification for new users after signup.
- [ ] -   **Two-Factor Authentication (2FA)**: Enhance login security with 2FA integration.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributers


-   **D1B** – Backend & Frontend Development (using Fastapi, MongoDB, React)
-   **Aymanoviche** – Backend Development (using Fastapi, MongoDB)

<a href="https://github.com/oussamafannouch/CrackAlyzer/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=oussamafannouch/CrackAlyzer" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License
This project is licensed under the MIT License - see the `LICENSE.txt` file for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Oussama Fannouch - [@OussamaFannouch](https://www.linkedin.com/in/oussamafannouch/) - oussamafannouch@gmail.com

Ayman Erroussi - [@ErroussiAyman](https://www.linkedin.com/in/ayman-erroussi/) - erroussiayman@gmail.com

Project Link: [https://github.com/OussamaFannouch/CrackAlyzer](https://github.com/OussamaFannouch/CrackAlyzer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments


We would like to thank the following for their contributions and support in making this project possible:

-   **Our Teacher**: A heartfelt thanks to our teacher for constantly supporting us on and providing the guidance and motivation to bring this project to life. Your encouragement made this project possible!
-   **Contributors**: A special thank you to all contributors for their time and effort in improving the project.

We also acknowledge all open-source projects and libraries used within this platform!

D1B x Aymanoviche
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/

