IF OBJECT_ID(N'[__EFMigrationsHistory]') IS NULL
BEGIN
    CREATE TABLE [__EFMigrationsHistory] (
        [MigrationId] nvarchar(150) NOT NULL,
        [ProductVersion] nvarchar(32) NOT NULL,
        CONSTRAINT [PK___EFMigrationsHistory] PRIMARY KEY ([MigrationId])
    );
END;
GO

BEGIN TRANSACTION;
GO

CREATE TABLE [Usuarios] (
    [Id] int NOT NULL IDENTITY,
    [Nome] nvarchar(max) NOT NULL,
    [Email] nvarchar(max) NOT NULL,
    [SenhaHash] nvarchar(max) NOT NULL,
    [Telefone] nvarchar(max) NULL,
    [Cargo] nvarchar(max) NOT NULL,
    [Permissao] int NOT NULL,
    CONSTRAINT [PK_Usuarios] PRIMARY KEY ([Id])
);
GO

CREATE TABLE [Chamados] (
    [Id] int NOT NULL IDENTITY,
    [Titulo] nvarchar(max) NOT NULL,
    [Descricao] nvarchar(max) NOT NULL,
    [DataAbertura] datetime2 NOT NULL,
    [DataFechamento] datetime2 NULL,
    [Solucao] nvarchar(max) NULL,
    [SolicitanteId] int NOT NULL,
    [TecnicoResponsavelId] int NULL,
    [Prioridade] int NOT NULL,
    [Status] int NOT NULL,
    [Tipo] nvarchar(max) NOT NULL,
    CONSTRAINT [PK_Chamados] PRIMARY KEY ([Id]),
    CONSTRAINT [FK_Chamados_Usuarios_SolicitanteId] FOREIGN KEY ([SolicitanteId]) 
    REFERENCES [Usuarios] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_Chamados_Usuarios_TecnicoResponsavelId] FOREIGN KEY ([TecnicoResponsavelId]) 
    REFERENCES [Usuarios] ([Id])
);
GO

CREATE TABLE [Historicos] (
    [Id] int NOT NULL IDENTITY,
    [Mensagem] nvarchar(max) NOT NULL,
    [DataOcorrencia] datetime2 NOT NULL,
    [EhMensagemDeIA] bit NOT NULL,
    [ChamadoId] int NOT NULL,
    [UsuarioId] int NULL,
    CONSTRAINT [PK_Historicos] PRIMARY KEY ([Id]),
    CONSTRAINT [FK_Historicos_Chamados_ChamadoId] FOREIGN KEY ([ChamadoId]) 
    REFERENCES [Chamados] ([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_Historicos_Usuarios_UsuarioId] FOREIGN KEY ([UsuarioId]) 
    REFERENCES [Usuarios] ([Id])
);
GO

CREATE INDEX [IX_Chamados_SolicitanteId] ON [Chamados] ([SolicitanteId]);
GO

CREATE INDEX [IX_Chamados_TecnicoResponsavelId] ON [Chamados] ([TecnicoResponsavelId]);
GO

CREATE INDEX [IX_Historicos_ChamadoId] ON [Historicos] ([ChamadoId]);
GO

CREATE INDEX [IX_Historicos_UsuarioId] ON [Historicos] ([UsuarioId]);
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20251103033711_InitialCreate', N'8.0.0');
GO

COMMIT;
GO

BEGIN TRANSACTION;
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20251103033758_InitialSchema', N'8.0.0');
GO

COMMIT;
GO

