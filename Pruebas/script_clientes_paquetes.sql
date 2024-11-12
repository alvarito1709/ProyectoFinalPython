

USE DB_USUARIOS;
GO

-- Crear la tabla clientes
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[compra_cliente]') AND type in (N'U'))
BEGIN
    CREATE TABLE compra_cliente (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_usuario INT,
        id_paquete INT,
		fecha_salida DATE

		FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
		FOREIGN KEY (id_paquete) REFERENCES paquetes(id_paquete)
    );
END
GO