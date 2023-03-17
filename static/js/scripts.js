// const sqlite = require('http://localhost:8080/sql-wasm.js');
import sqlite from './sql-wasm.js';


const db = new sqlite.Database('biblia_con_comentario.db');

function buscarVersiculo(libro, capitulo, versiculo) {
    texto="";
    comentario=""

    texto=db.get(
      `SELECT texto FROM versiculos WHERE libro = ? AND capitulo = ? AND versiculo = ?`,
      [libro, capitulo, versiculo],
      (err, row) => {
        if (err) {
          console.error(err.message);
        } else {
          console.log(row.texto);
        }
      }
    );

    comentario=db.get(
        `SELECT comentario FROM versiculos WHERE libro = ? AND capitulo = ? AND versiculo = ?`,
        [libro, capitulo, versiculo],
        (err, row) => {
          if (err) {
            console.error(err.message);
          } else {
            console.log(row.texto);
          }
        }
      );
  }