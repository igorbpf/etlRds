create table Especialista
(
  id int NOT NULL
  AUTO_INCREMENT,
  funcional int NOT NULL UNIQUE,
  nome varchar
  (255) NOT NULL,
  PRIMARY KEY
  (id)
);

  create table Cliente
  (
    agencia int NOT NULL,
    conta int NOT NULL,
    nome varchar(255) NOT NULL,
    saldo float NOT NULL,
    especialista_id int NOT NULL,
    data_hora_encarteiramento DATETIME NOT NULL,
    data_encarteiramento DATE NOT NULL,
    horario_encarteiramento TIME NOT NULL,
    PRIMARY KEY (agencia, conta),
    FOREIGN KEY (especialista_id) REFERENCES Especialista(funcional)
  );

