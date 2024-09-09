-- queries
INSERT INTO usuarios (usuario_email, usuario_password, usuario_rut, usuario_nombre)
VALUES ('dcortes@gmail.com', '123', '17811265-1', 'Diego Cortes');

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


ALTER TABLE "usuarios"
ADD COLUMN "usuario_nombre" VARCHAR(255),
ADD CONSTRAINT "unique_usuario_email" UNIQUE ("usuario_email"),
ADD CONSTRAINT "unique_usuario_rut" UNIQUE ("usuario_rut")

UPDATE "usuarios"
SET "usuario_nombre" = 
    CASE 
        WHEN "usuario_id" = '8347b9c9-99e5-42b2-89c6-0768f9144e5a' THEN 'Jen'
        WHEN "usuario_id" = '241fcbf4-4fa8-40a7-a609-98049ee6a4b7' THEN 'Max Ihnen'
        WHEN "usuario_id" = 'cc5ff97b-14b0-4983-9260-236d75694fa8' THEN 'Example Name'
        WHEN "usuario_id" = 'b64721d5-1693-4a24-9f23-9851a87ce8eb' THEN 'Diego Cortés'
    END
WHERE "usuario_id" IN (
    '8347b9c9-99e5-42b2-89c6-0768f9144e5a',
    '241fcbf4-4fa8-40a7-a609-98049ee6a4b7',
    'cc5ff97b-14b0-4983-9260-236d75694fa8',
    'b64721d5-1693-4a24-9f23-9851a87ce8eb'
);


-- Insertar un usuario de prueba 
INSERT INTO usuarios (usuario_email, usuario_password, usuario_rut, usuario_nombre)
VALUES ('productor@filmhub.com', 'contraseña_hasheada', '12345678-9', 'Ana Productora');

DO $$
DECLARE
    id_usuario UUID;
    id_cliente UUID;
    id_proyecto UUID;
BEGIN
    SELECT usuario_id INTO id_usuario FROM usuarios WHERE usuario_email = 'productor@filmhub.com';

    INSERT INTO clientes (usuario_id, cliente_nombre, cliente_email, cliente_tel, cliente_rut)
    VALUES (id_usuario, 'Ridley Scott', 'ridley.scott@dreamworks.com', '123456789', '98765432-1')
    RETURNING cliente_id INTO id_cliente;

    INSERT INTO proyectos (usuario_id, cliente_id, proyecto_nombre, proyecto_presupuesto, proyecto_inicio, proyecto_termino, proyecto_descripcion, proyecto_tipo)
    VALUES (
        id_usuario, 
        id_cliente, 
        'El Gladiador', 
        103000000.00, 
        '1999-01-01'::DATE, 
        '2000-05-01'::DATE, 
        'Película épica de drama histórico dirigida por Ridley Scott y protagonizada por Russell Crowe', 
        'Producción de Cine'
    )
    RETURNING proyecto_id INTO id_proyecto;

    INSERT INTO tareas (proyecto_id, tarea_nombre, tarea_fecha, tarea_descripcion, tarea_completada, tarea_necesita_pago)
    VALUES
    (id_proyecto, 'Contratar a Russell Crowe como Máximo', CURRENT_DATE + INTERVAL '1 day', 'Finalizar contrato y programación para Russell Crowe', FALSE, TRUE),
    (id_proyecto, 'Asegurar locaciones de filmación en Marruecos', CURRENT_DATE + INTERVAL '1 day', 'Obtener permisos y finalizar acuerdos para filmar en Marruecos', FALSE, TRUE),
    (id_proyecto, 'Reunión de diseño de vestuario', CURRENT_DATE + INTERVAL '1 day', 'Reunirse con Janty Yates para discutir los diseños de vestuario', FALSE, FALSE),
    (id_proyecto, 'Finalizar guion', CURRENT_DATE + INTERVAL '2 days', 'Revisión final y aprobación del guion por David Franzoni, John Logan y William Nicholson', FALSE, TRUE),
    (id_proyecto, 'Comenzar construcción de escenarios', CURRENT_DATE + INTERVAL '3 days', 'Iniciar la construcción del set del Coliseo en Malta', FALSE, TRUE),
    (id_proyecto, 'Coreografiar escenas de batalla', CURRENT_DATE + INTERVAL '5 days', 'Trabajar con el coordinador de escenas de riesgo en las secuencias de lucha', FALSE, FALSE),
    (id_proyecto, 'Composición musical de Hans Zimmer', CURRENT_DATE + INTERVAL '10 days', 'Verificar el progreso de la banda sonora', FALSE, TRUE);

END $$;