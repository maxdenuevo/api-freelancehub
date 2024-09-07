
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
import hashlib
from flask_cors import CORS  
import jwt
from flask_mail import Mail, Message

load_dotenv()
app = Flask(__name__)
CORS(app)

jwt_secret = os.getenv("JWT_SECRET")

connection = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    cursor_factory=RealDictCursor
)


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = (os.getenv("MAIL_DEFAULT_SENDER"), os.getenv("MAIL_DEFAULT_SENDER_EMAIL"))

@app.route('/')
def home():
    return 'Hello, Freelancers'

@app.route('/register-usuario', methods=['POST'])
def register_usuario():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        email = body.get('usuario_email')
        rut = body.get('usuario_rut')
        password = body.get('usuario_password')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        cursor.execute("""
            INSERT INTO usuarios (usuario_email, usuario_password, usuario_rut)
            VALUES (%s, %s, %s) RETURNING usuario_id
        """, [email, hashed_password, rut])

        usuario_id = cursor.fetchone().get('usuario_id')
        connection.commit()
        return jsonify({"message": "Usuario creado correctamente", "usuario_id": usuario_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear usuario"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/login-usuario', methods=['POST'])
def login_usuario():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        email = body.get('usuario_email')
        password = body.get('usuario_password')

        cursor.execute("SELECT * FROM usuarios WHERE usuario_email = %s", [email])
        result = cursor.fetchone()
        if not result:
            return jsonify({"message": "Usuario no encontrado"}), 404

        hashed_password = result.get('usuario_password')
        if hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password:
            token = jwt.encode({
                "usuario_id": result.get('usuario_id'),
                "usuario_email": result.get('usuario_email')
            }, jwt_secret, algorithm='HS256')

            return jsonify({"message": "Usuario autenticado correctamente", "token": token}), 200
        return jsonify({"message": "Credenciales inválidas"}), 401
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al autenticar usuario"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/create-cliente', methods=['POST'])
def create_cliente():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        usuario_id = body.get('usuario_id')
        nombre = body.get('cliente_nombre')
        email = body.get('cliente_email')
        tel = body.get('cliente_tel')
        rut = body.get('cliente_rut')

        cursor.execute("""
            INSERT INTO clientes (usuario_id, cliente_nombre, cliente_email, cliente_tel, cliente_rut)
            VALUES (%s, %s, %s, %s, %s) RETURNING cliente_id
        """, [usuario_id, nombre, email, tel, rut])

        cliente_id = cursor.fetchone().get('cliente_id')
        connection.commit()
        return jsonify({"message": "Cliente creado correctamente", "cliente_id": cliente_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear cliente"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/create-proyecto', methods=['POST'])
def create_proyecto():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        usuario_id = body.get('usuario_id')
        cliente_id = body.get('cliente_id')
        nombre = body.get('proyecto_nombre')
        presupuesto = body.get('proyecto_presupuesto')
        inicio = body.get('proyecto_inicio')
        termino = body.get('proyecto_termino')
        descripcion = body.get('proyecto_descripcion')
        tipo = body.get('proyecto_tipo')
        print(usuario_id, cliente_id, nombre, presupuesto, inicio, termino, descripcion, tipo)
        cursor.execute("""
            INSERT INTO proyectos (usuario_id, cliente_id, proyecto_nombre, proyecto_presupuesto, proyecto_inicio, proyecto_termino, proyecto_descripcion, proyecto_tipo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING proyecto_id
        """, [usuario_id, cliente_id, nombre, presupuesto, inicio, termino, descripcion, tipo])

        proyecto_id = cursor.fetchone().get('proyecto_id')
        connection.commit()
        return jsonify({"message": "Proyecto creado correctamente", "proyecto_id": proyecto_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear proyecto"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/create-tarea', methods=['POST'])
def create_tarea():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        proyecto_id = body.get('proyecto_id')
        nombre = body.get('tarea_nombre')
        fecha = body.get('tarea_fecha')
        descripcion = body.get('tarea_descripcion')
        completada = body.get('tarea_completada')
        necesita_pago = body.get('tarea_necesita_pago')
        fecha_recordatorio = body.get('tarea_fecha_recordatorio')  

        cursor.execute("""
            INSERT INTO tareas (proyecto_id, tarea_nombre, tarea_fecha, tarea_descripcion, tarea_completada, tarea_necesita_pago, tarea_fecha_recordatorio)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING tarea_id
        """, [proyecto_id, nombre, fecha, descripcion, completada, necesita_pago, fecha_recordatorio])

        tarea_id = cursor.fetchone().get('tarea_id')
        connection.commit()
        return jsonify({"message": "Tarea creada correctamente", "tarea_id": tarea_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear tarea"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/create-pago', methods=['POST'])
def create_pago():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        tarea_id = body.get('tarea_id')
        pago_monto = body.get('pago_monto')
        pago_fecha = body.get('pago_fecha')
        pago_completado = body.get('pago_completado')
        pago_comprobante = body.get('pago_comprobante')

        cursor.execute("""
            INSERT INTO pagos (tarea_id, pago_monto, pago_fecha, pago_completado, pago_comprobante)
            VALUES (%s, %s, %s, %s, %s) RETURNING pago_id
        """, [tarea_id, pago_monto, pago_fecha, pago_completado, pago_comprobante])

        pago_id = cursor.fetchone().get('pago_id')
        connection.commit()
        return jsonify({"message": "Pago creado correctamente", "pago_id": pago_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear pago"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get-pago/<string:pago_id>', methods=['GET'])
def get_pago(pago_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pagos WHERE pago_id = %s", [str(pago_id)])
        result = cursor.fetchone()
        if result:
            return jsonify({"pago": result}), 200
        else:
            return jsonify({"message": "Pago no existe"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener pago"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get-usuario/<string:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", [str(user_id)])
        result = cursor.fetchone()
        if result:
            return jsonify({"usuario": result}), 200
        else:
            return jsonify({"message": "Usuario no existe"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener usuario"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/create-plantilla', methods=['POST'])
def create_plantilla():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        plantilla_nombre = body.get('plantilla_nombre')

        cursor.execute("""
            INSERT INTO plantillas (plantilla_nombre)
            VALUES (%s) RETURNING plantilla_id
        """, [plantilla_nombre])

        plantilla_id = cursor.fetchone().get('plantilla_id')
        connection.commit()
        return jsonify({"message": "Plantilla creada correctamente", "plantilla_id": plantilla_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear plantilla"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/create-contrato', methods=['POST'])
def create_contrato():
    cursor = connection.cursor()
    try:
        body = request.get_json()
        cliente_id = body.get('cliente_id')
        plantilla_id = body.get('plantilla_id')
        proyecto_id = body.get('proyecto_id')

        cursor.execute("""
            INSERT INTO contratos (cliente_id, plantilla_id, proyecto_id)
            VALUES (%s, %s, %s) RETURNING contrato_id
        """, [cliente_id, plantilla_id, proyecto_id])

        contrato_id = cursor.fetchone().get('contrato_id')
        connection.commit()
        return jsonify({"message": "Contrato creado correctamente", "contrato_id": contrato_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al crear contrato"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get-contrato/<string:contrato_id>', methods=['GET'])
def get_contrato(contrato_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM contratos WHERE contrato_id = %s", [str(contrato_id)])
        result = cursor.fetchone()
        if result:
            return jsonify({"contrato": result}), 200
        else:
            return jsonify({"message": "Contrato no existe"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener contrato"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/proyectos/<string:user_id>', methods=['GET'])
def get_proyectos(user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM proyectos where usuario_id = %s", [user_id])
        proyectos = cursor.fetchall()
        return jsonify({"proyectos": proyectos}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo proyecto"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/proyecto/<string:proyecto_id>', methods=['GET'])
def get_proyecto(proyecto_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM proyectos WHERE proyecto_id = %s", [str(proyecto_id)])
        proyecto = cursor.fetchone()
        if proyecto:
            return jsonify({"proyecto": proyecto}), 200
        else:
            return jsonify({"message": "Project not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error fetching project"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/proyecto/<string:proyecto_id>', methods=['PATCH'])
def update_proyecto(proyecto_id):
    cursor = connection.cursor()
    try:
        body = request.get_json()
        fields = ', '.join([f"{k} = %s" for k in body.keys()])
        values = list(body.values())
        values.append(str(proyecto_id))

        cursor.execute(f"""
            UPDATE proyectos SET {fields} WHERE proyecto_id = %s
        """, values)
        connection.commit()

        return jsonify({"message": "Proyecto actualizado"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error actualizando proyecto"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/proyecto/<string:proyecto_id>', methods=['DELETE'])
def delete_proyecto(proyecto_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM proyectos WHERE proyecto_id = %s", [str(proyecto_id)])
        connection.commit()
        return jsonify({"message": "Proyecto eliminado"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error eliminando proyecto"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/tareas', methods=['GET'])
def get_tareas():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        return jsonify({"tareas": tareas}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo tareas"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/tarea/<string:tarea_id>', methods=['GET'])
def get_tarea(tarea_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM tareas WHERE tarea_id = %s", [str(tarea_id)])
        tarea = cursor.fetchone()
        if tarea:
            return jsonify({"tarea": tarea}), 200
        else:
            return jsonify({"message": "Tarea no encontrada"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo tareas"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/tarea/<string:tarea_id>', methods=['PATCH'])
def update_tarea(tarea_id):
    cursor = connection.cursor()
    try:
        body = request.get_json()
        fields = ', '.join([f"{k} = %s" for k in body.keys()])
        values = list(body.values())
        values.append(str(tarea_id))

        cursor.execute(f"""
            UPDATE tareas SET {fields} WHERE tarea_id = %s
        """, values)
        connection.commit()

        return jsonify({"message": "Tarea actualizada"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error actualizando tarea"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/tarea/<string:tarea_id>', methods=['DELETE'])
def delete_tarea(tarea_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM tareas WHERE tarea_id = %s", [str(tarea_id)])
        connection.commit()
        return jsonify({"message": "Tarea eliminada"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error eliminando tarea"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/pagos', methods=['GET'])
def get_pagos():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pagos")
        pagos = cursor.fetchall()
        return jsonify({"pagos": pagos}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo pagos"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/pago/<string:pago_id>', methods=['PATCH'])
def update_pago(pago_id):
    cursor = connection.cursor()
    try:
        body = request.get_json()
        fields = ', '.join([f"{k} = %s" for k in body.keys()])
        values = list(body.values())
        values.append(str(pago_id))

        cursor.execute(f"""
            UPDATE pagos SET {fields} WHERE pago_id = %s
        """, values)
        connection.commit()

        return jsonify({"message": "Pago actualizado exitosamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error actualizando pago"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/pago/<string:pago_id>', methods=['DELETE'])
def delete_pago(pago_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM pagos WHERE pago_id = %s", [str(pago_id)])
        connection.commit()
        return jsonify({"message": "Pago eliminado"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error eliminando pago"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/pago/<string:pago_id>', methods=['GET'])
def get_specific_pago(pago_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM pagos WHERE pago_id = %s", [str(pago_id)])
        pago = cursor.fetchone()
        if pago:
            return jsonify({"pago": pago}), 200
        else:
            return jsonify({"message": "Pago no encontrado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error encontrando pago"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/clientes', methods=['GET'])
def get_clientes():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        return jsonify({"clientes": clientes}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error fetching clients"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/cliente/<string:cliente_id>', methods=['PATCH'])
def update_cliente(cliente_id):
    cursor = connection.cursor()
    try:
        body = request.get_json()
        fields = ', '.join([f"{k} = %s" for k in body.keys()])
        values = list(body.values())
        values.append(str(cliente_id))

        cursor.execute(f"""
            UPDATE clientes SET {fields} WHERE cliente_id = %s
        """, values)
        connection.commit()

        return jsonify({"message": "Cliente actualizado correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al actualizar cliente"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/cliente/<string:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE cliente_id = %s", [str(cliente_id)])
        connection.commit()
        return jsonify({"message": "Cliente eliminado correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al eliminar cliente"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/cliente/<string:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM clientes WHERE cliente_id = %s", [str(cliente_id)])
        cliente = cursor.fetchone()
        if cliente:
            return jsonify({"cliente": cliente}), 200
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener cliente"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/plantilla/<string:plantilla_id>', methods=['PATCH'])
def update_plantilla(plantilla_id):
    cursor = connection.cursor()
    try:
        body = request.get_json()
        fields = ', '.join([f"{k} = %s" for k in body.keys()])
        values = list(body.values())
        values.append(str(plantilla_id))

        cursor.execute(f"""
            UPDATE plantillas SET {fields} WHERE plantilla_id = %s
        """, values)
        connection.commit()

        return jsonify({"message": "Plantilla actualizada correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al actualizar plantilla"}), 500
    finally:
        cursor.close()
        connection.close()

app.route('/plantilla/<string:plantilla_id>', methods=['DELETE'])
def delete_plantilla(plantilla_id):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM plantillas WHERE plantilla_id = %s", [str(plantilla_id)])
        connection.commit()
        return jsonify({"message": "Plantilla eliminada correctamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al eliminar plantilla"}), 500
    finally:
        cursor.close()
        connection.close()
 

app.route('/plantilla/<string:plantilla_id>', methods=['GET'])
def get_plantilla(plantilla_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM plantillas WHERE plantilla_id = %s", [str(plantilla_id)])
        plantilla = cursor.fetchone()
        if plantilla:
            return jsonify({"plantilla": plantilla}), 200
        else:
            return jsonify({"message": "Plantilla no encontrada"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener plantilla"}), 500
    finally:
        cursor.close()
        connection.close()    

# /clientes/<string:usuario_id>
@app.route('/clientes/<string:usuario_id>', methods=['GET'])
def get_clientes_by_usuario(usuario_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM clientes WHERE usuario_id = %s", [usuario_id])
        clientes = cursor.fetchall()
        return jsonify({"clientes": clientes}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo clientes"}), 500
    finally:
        cursor.close()
        connection.close()

# /contratos/<string:proyecto_id>
@app.route('/contratos/<string:proyecto_id>', methods=['GET'])
def get_contratos_by_proyecto(proyecto_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM contratos WHERE proyecto_id = %s", [proyecto_id])
        contratos = cursor.fetchall()
        return jsonify({"contratos": contratos}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo contratos"}), 500
    finally:
        cursor.close()
        connection.close()

# /pagos/<string:proyecto_id>
@app.route('/pagos/<string:proyecto_id>', methods=['GET'])
def get_pagos_by_proyecto(proyecto_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT p.* 
            FROM pagos p
            JOIN tareas t ON p.tarea_id = t.tarea_id
            WHERE t.proyecto_id = %s
        """, [proyecto_id])
        pagos = cursor.fetchall()
        return jsonify({"pagos": pagos}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo pagos"}), 500
    finally:
        cursor.close()
        connection.close()

# /tareas/<string:proyecto_id>
@app.route('/tareas/<string:proyecto_id>', methods=['GET'])
def get_tareas_by_proyecto(proyecto_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM tareas WHERE proyecto_id = %s", [proyecto_id])
        tareas = cursor.fetchall()
        return jsonify({"tareas": tareas}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error trayendo tareas"}), 500
    finally:
        cursor.close()
        connection.close()

# /usuarios/<string:usuario_id>/update-password
@app.route('/usuario/<string:usuario_id>/update-password', methods=['PATCH'])
def update_usuario_password(usuario_id):
    cursor = connection.cursor()
    try:
        body = request.get_json()
        current_password = body.get('current_password')
        new_password = body.get('new_password')

        if not current_password or not new_password:
            return jsonify({"message": "Contraseña actual y nueva son requeridas"}), 400

        # revisa la contraseña actual
        cursor.execute("SELECT usuario_password FROM usuarios WHERE usuario_id = %s", [usuario_id])
        result = cursor.fetchone()
        if not result:
            return jsonify({"message": "Usuario no encontrado"}), 404

        stored_password = result['usuario_password']
        if hashlib.sha256(current_password.encode('utf-8')).hexdigest() != stored_password:
            return jsonify({"message": "Contraseña actual incorrecta"}), 401

        # actualiza con una contraseña nueva
        hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        cursor.execute("""
            UPDATE usuarios SET usuario_password = %s WHERE usuario_id = %s
        """, [hashed_new_password, usuario_id])
        connection.commit()

        return jsonify({"message": "Contraseña actualizada exitosamente"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al actualizar la contraseña"}), 500
    finally:
        cursor.close()
        connection.close()        


mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    body = request.get_json()
    email = Message(
        subject=body.get('subject'),
        recipients=body.get('recipients'),
        body=body.get('body')
    )
    mail.send(email)
    return jsonify({"message": "Email enviado correctamente!"}), 200


# app.run(host='0.0.0.0', port=3000, debug=True)
# app.run(ssl_context='adhoc', debug=True)
