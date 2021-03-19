create table Especialista
(
  funcional int NOT NULL,
  nome varchar(255) NOT NULL,
  PRIMARY KEY (funcional)
);

create table Cliente
(
  agencia int NOT NULL,
  conta int NOT NULL,
  nome varchar(255) NOT NULL,
  saldo float NOT NULL,
  especialista_id int NOT NULL,
  PRIMARY KEY (agencia, conta),
  FOREIGN KEY (especialista_id) REFERENCES Especialista(funcional)
);

