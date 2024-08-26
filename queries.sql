-- queries
INSERT INTO usuarios (usuario_email, usuario_password, usuario_rut)
VALUES ('dcortes@gmail.com', '123', '17811265-1');

INSERT INTO clientes (usuario_id, cliente_nombre, cliente_email, cliente_tel, cliente_rut)
VALUES ('8b6b20fa-1d7f-472c-ab6a-4f89271114f4', 'elon musk','elon@tesla.com', '123', '17265-1');

INSERT INTO proyectos (usuario_id, proyecto_nombre, proyecto_presupuesto, proyecto_inicio, proyecto_termino, proyecto_descripcion, proyecto_tipo, cliente_id)
VALUES ('8b6b20fa-1d7f-472c-ab6a-4f89271114f4', 'pawPals', '500', '2024-07-01', '2024-07-30', 'app para lucir a tu mascota, va a tener mil funcionalides.', 'consultoria', '74b53893-3f05-4d9d-9a0e-c11afe7b2f8b');

INSERT INTO tareas (proyecto_id, tarea_nombre, tarea_fecha, tarea_descripcion, tarea_completada, tarea_necesita_pago)
VALUES ('cd63c8e4-9574-4c93-8228-1ab946d099a0', 'creacion del back', '2024-07-02', 'crear SQL y probar en postgres', FALSE, TRUE)

INSERT INTO pagos (tarea_id, pago_monto, pago_fecha, pago_completado, pago_comprobante)
VALUES ('097dcaa0-c5ea-4583-bbdb-7864b33c144b', '100', FALSE, 'wwww.algo.com/comprobante.jpg')

INSERT INTO plantillas (plantilla_nombre)
VALUES ('honorarios consultoria')

INSERT INTO contratos (cliente_id, plantilla_id, proyecto_id)
VALUES ('74b53893-3f05-4d9d-9a0e-c11afe7b2f8b', '2c012ba8-1af0-4f62-bfaf-b4933018edd6', 'cd63c8e4-9574-4c93-8228-1ab946d099a0')
