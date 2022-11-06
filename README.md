# IngressWorkerClientDemo
This is a system that has an ingress worker and client communicating to one another to send files

\section{Instructions}
\subsection{Docker set up}
\begin{lstlisting}[caption={[Sample Code 2]My csnetimage}, label={lst:snippet2}]
FROM ubuntu
WORKDIR /compnets
RUN apt-get update
RUN apt-get install -y net-tools netcat tcpdump inetutils-ping python3
RUN apt-get install -y vim
RUN apt-get install -y git
RUN apt-get install -y python3-pip --fix-missing
RUN pip install tqdm -y

CMD ["/bin/bash"]
\end{lstlisting}


Once docker is set up make two docker networks
\begin{lstlisting}[caption={[Sample Code 2]Set up instructions}, label={lst:snippet2}]
docker network create -d bridge --subnet 172.21.0.0/16 internalnetwork
docker network create -d bridge --subnet 172.20.0.0/16 externalnetwork
docker build -t csnetimage .
docker create -ti --name ingress --cap-add=all -v ~/compnets:/compnets 
csnetimage /bin/bash
docker create -ti --name client0 --cap-add=all -v ~/compnets:/compnets 
csnetimage /bin/bash
docker create -ti --name worker0 --cap-add=all -v ~/compnets:/compnets 
csnetimage /bin/bash
docker create -ti --name worker1 --cap-add=all -v ~/compnets:/compnets 
csnetimage /bin/bash
docker create -ti --name worker2 --cap-add=all -v ~/compnets:/compnets 
csnetimage /bin/bash
docker network connect ingress internalnetwork
docker network connect ingress externalnetwork
docker network connect client0 externalnetwork
docker network connect worker0 internalnetwork
docker network connect worker1 internalnetwork
docker network connect worker2 internalnetwork
\end{lstlisting}

On separate terminal start all of the containers 
Firstly start the ingress and insert the files using "docker cp" command.
Order does matter here (top to bottom)
\begin{lstlisting}[caption={[Sample Code 2] Ingress}, label={lst:snippet2}]
    docker start -i ingress
    docker cp ./sourcefiles CONTAINER:/work
    python3 ArshadMohammed_server.py
\end{lstlisting}

\begin{lstlisting}[caption={[Sample Code 2]Client 0}, label={lst:snippet2}]
    docker start -i client0
    python3 ArshadMohammed_client.py
\end{lstlisting}

\begin{lstlisting}[caption={[Sample Code 2]Worker 0}, label={lst:snippet2}]
    docker start -i worker0
    python3 ArshadMohammed_worker0.py
\end{lstlisting}

\begin{lstlisting}[caption={[Sample Code 2]Worker 1}, label={lst:snippet2}]
    docker start -i worker1
    python3 ArshadMohammed_worker1.py
\end{lstlisting}

\begin{lstlisting}[caption={[Sample Code 2]Worker 2}, label={lst:snippet2}]
    docker start -i worker2
    python3 ArshadMohammed_worker2.py
\end{lstlisting}
