DROP DATABASE IF EXISTS `devolucion_muestra`;
CREATE DATABASE `devolucion_muestra`;
USE devolucion_muestra;

DROP TABLE IF EXISTS `comentario`;
CREATE TABLE `comentario` (
  `id_comentario` int NOT NULL auto_increment,
  `proyecto` varchar(50) NOT NULL,
  `comentario` longtext NOT NULL,
  PRIMARY KEY (`id_comentario`)
);
DROP TABLE IF EXISTS `ingresante`;
CREATE TABLE `ingresante` (
  `id_ingresante` int NOT NULL auto_increment,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `mail` varchar(30) NOT NULL,
  `carrera` varchar(50) NOT NULL,
  PRIMARY KEY (`id_ingresante`)
);