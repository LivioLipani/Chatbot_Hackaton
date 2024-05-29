<a name="readme-top"></a>
# Chatbot Nico - Hackathon Edition

<details>
    <summary>Table of Contents</summary>
    <li><a href="#about-the-project">About the project</a></li>
    <li><a href="#Built-With">Built With</a></li>
    <li><a href="#Contributing">Contributing</a></li>
  </ol>
</details>

## About The Project
### What it does
Nico è un chatbot intelligente che semplifica e velocizza la creazione dei preventivi di stima.

### How we built it
Abbiamo utilizzato LangChain per implementare la tecnologia RAG. Grazie agli strumenti forniti dal framework, siamo riusciti a gestire diversi task del chatbot e a memorizzare i dati in cloud. Parallelamente, abbiamo creato un database per gestire le informazioni aziendali e confrontare i feedback degli utenti con quelli del chatbot.

### Challenges we ran into
I task più ardui sono stati: 1) l'addestramento del chatbot affinché si concentrasse sullo scopo; 2) la gestione di un VectorStore in cloud; 3) implementazione della possibilità, per l'utente, di richiedere di parlare con un operatore; 4) gestione di un sistema di feedback da parte dell'utente e da parte dell'LLM, compresa la memorizzazione di tali informazioni in un db SQLite locale.

### Accomplishments that we're proud of
Siamo veramente fieri del risultato raggiunto nonostante il poco tempo, dell'interfaccia che abbiamo costruito e delle integrazioni che siamo riusciti ad implementare in modo efficiente. Abbiamo inoltre avuto modo di apprendere, in modo abbastanza approfondito, quali sono le dinamiche che si celano dietro la creazione di un chatbot.

### What we learned
L'uso di VectorStore cloud e la definizione di tool e creazione di tool custom.

### What's next for Nico - The Cost Estimator
Nico ha ancora un grandissimo margine di miglioramento, dalla gestione accurata delle richieste alla memorizzazione efficiente dei dati.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Built With

* [![LangChain][langchain.com]][LangChain-url]
* [![Openai][openai.com]][Openai-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>








## Contributing

Antonino Palumeri
https://www.linkedin.com/in/antonino-palumeri-0048bb247/

Eleonora Giuffrida
https://www.linkedin.com/in/eleonora-giuffrida-7795a130b/

Livio Mattia Lipani
https://www.linkedin.com/in/livio-mattia-lipani/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

![LangChain.com](https://img.shields.io/badge/%F0%9F%A6%9C%EF%B8%8F%F0%9F%94%97LangChain-LangChain)
[LangChain-url]: https://www.langchain.com/
[Openai.com]: https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/OpenAI_Logo.svg/1200px-OpenAI_Logo.svg.png
[Openai-url]: https://openai.com


