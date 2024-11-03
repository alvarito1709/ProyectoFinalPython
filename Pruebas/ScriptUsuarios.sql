-- Crear la base de datos DBCLIENTES si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DB_USUARIOS')
BEGIN
    CREATE DATABASE DB_USUARIOS;
END
GO

-- Usar la base de datos DBCLIENTES
USE DB_USUARIOS;
GO

-- Crear la tabla clientes
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[usuarios]') AND type in (N'U'))
BEGIN
    CREATE TABLE usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        usuario NVARCHAR(50),
        contrase�a NVARCHAR(50),
        rol INT,
        email NVARCHAR(100)
    );
END
GO

-- Insertar 20 registros de ejemplo
INSERT INTO usuarios(usuario, contrase�a, rol, email) VALUES
('Pepito', '123', '1', 'juan@example.com'),
('Fulano', '12345', '0', 'maria@example.com'),
('Carlos', 'perro', '0', 'carlos@example.com'),
('Emilio', '123Roger', '1', 'emaidana@frba.utn.edu.ar');
GO

-- Seleccionar todos los registros de la tabla clientes
SELECT * FROM usuarios;
GO
