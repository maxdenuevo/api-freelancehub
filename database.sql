
-- database.sql
CREATE TABLE "usuarios"(
    "usuario_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "usuario_email" VARCHAR(255) NOT NULL,
    "usuario_password" VARCHAR(255) NOT NULL,
    "usuario_rut" VARCHAR(255) NOT NULL
);

CREATE TABLE "clientes"(
    "cliente_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "usuario_id" UUID NOT NULL,
    "cliente_nombre" VARCHAR(255) NOT NULL,
    "cliente_email" VARCHAR(255) NOT NULL,
    "cliente_tel" VARCHAR(255) NOT NULL,
    "cliente_rut" VARCHAR(255) NOT NULL,
    CONSTRAINT "clientes_usuario_id_foreign" FOREIGN KEY("usuario_id") REFERENCES "usuarios"("usuario_id")
);

CREATE TABLE "proyectos"(
    "proyecto_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "usuario_id" UUID NOT NULL,
    "proyecto_nombre" VARCHAR(255) NOT NULL,
    "proyecto_presupuesto" DECIMAL(8, 2) NOT NULL,
    "proyecto_inicio" DATE NOT NULL,
    "proyecto_termino" DATE NOT NULL,
    "proyecto_descripcion" TEXT NOT NULL,
    "proyecto_tipo" VARCHAR(255) NOT NULL,
    "cliente_id" UUID NOT NULL,
    CONSTRAINT "proyectos_usuario_id_foreign" FOREIGN KEY("usuario_id") REFERENCES "usuarios"("usuario_id"),
    CONSTRAINT "proyectos_cliente_id_foreign" FOREIGN KEY("cliente_id") REFERENCES "clientes"("cliente_id")
);

CREATE TABLE "tareas"(
    "tarea_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "proyecto_id" UUID NOT NULL,
    "tarea_nombre" VARCHAR(255) NOT NULL,
    "tarea_fecha" DATE NOT NULL,
    "tarea_descripcion" TEXT NOT NULL,
    "tarea_completada" BOOLEAN NOT NULL,
    "tarea_necesita_pago" BOOLEAN NOT NULL,
    CONSTRAINT "tareas_proyecto_id_foreign" FOREIGN KEY("proyecto_id") REFERENCES "proyectos"("proyecto_id")
);

CREATE TABLE "pagos"(
    "pago_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "tarea_id" UUID NOT NULL,
    "pago_monto" DECIMAL(8, 2) NOT NULL,
    "pago_fecha" DATE NOT NULL,
    "pago_completado" BOOLEAN NOT NULL,
    "pago_comprobante" TEXT NULL,
    CONSTRAINT "pagos_tarea_id_foreign" FOREIGN KEY("tarea_id") REFERENCES "tareas"("tarea_id")
);


CREATE TABLE "plantillas"(
    "plantilla_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "plantilla_nombre" VARCHAR(255) NOT NULL
);

CREATE TABLE "contratos"(
    "contrato_id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "cliente_id" UUID NOT NULL,
    "plantilla_id" UUID NOT NULL,
    "proyecto_id" UUID NOT NULL,
    CONSTRAINT "contratos_proyecto_id_foreign" FOREIGN KEY("proyecto_id") REFERENCES "proyectos"("proyecto_id"),
    CONSTRAINT "contratos_cliente_id_foreign" FOREIGN KEY("cliente_id") REFERENCES "clientes"("cliente_id")
);