/* ============================================================================
   REFERÊNCIA: Estrutura das Tabelas Utilizadas
   ============================================================================
   
   Este documento detalha as tabelas e colunas usadas na consulta de
   atendimentos 663 finalizados.
   ============================================================================ */

-- ============================================================================
-- TABELA 1: HATENDIMENTOBASE (Cabeçalho do Atendimento)
-- ============================================================================
-- Descrição: Registra o atendimento/requerimento acadêmico

-- Colunas principais:
-- CODCOLIGADA (smallint)        → Coligada (sempre 1 = UNINTA)
-- CODATENDIMENTO (int)          → ID único do atendimento
-- CODLOCAL (int)                → Localidade onde foi registrado
-- CODTIPOATENDIMENTO (int)      → Tipo (663 = Rematrícula)
-- ABERTURA (datetime)           → Data/hora que foi aberto
-- FECHAMENTO (datetime)         → Data/hora que foi fechado
-- CODSTATUS (varchar)           → Status atual do atendimento
-- RECMODIFIEDBY (varchar)       → Último usuário que modificou
-- RECMODIFIEDON (datetime)      → Data da última modificação


-- ============================================================================
-- TABELA 2: HHISTORICOETAPASATENDIMENTO (Histórico de Etapas)
-- ============================================================================
-- Descrição: Rastreia por qual etapa o atendimento passou e quem processou

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- CODATENDIMENTO (int)              → ID do atendimento (FK → HATENDIMENTOBASE)
-- CODETAPAANTERIOR (int)            → Etapa anterior por qual passou
-- CODETAPAATUAL (int)               → Etapa atual
-- CODATENDENTEANTERIOR (int)        → Quem processou antes
-- CODATENDENTEATUAL (int)           → Quem está processando agora
-- MUDANCADEETAPA (datetime)         → Quando mudou de etapa
-- RECCREATEDBY (varchar)            → Quem criou este registro
-- RECCREATEDON (datetime)           → Quando foi criado


-- ============================================================================
-- TABELA 3: SATENDIMENTO (Dados Acadêmicos do Atendimento)
-- ============================================================================
-- Descrição: Dados específicos do aluno e curso no atendimento

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- CODATENDIMENTO (int)              → ID do atendimento (FK → HATENDIMENTOBASE)
-- CODLOCAL (int)                    → Local (FK → HATENDIMENTOBASE)
-- RA (varchar)                      → Registro Acadêmico do aluno
-- CODPROF (varchar)                 → Código do professor (se aplicável)
-- IDHABILITACAOFILIAL (int)         → FK → SHABILITACAOFILIAL (curso/polo)
-- IDPERLET (int)                    → FK → SPLETIVO (período letivo)
-- IDTURMADISC (int)                 → FK → STURMADISC (disciplina, se aplicável)


-- ============================================================================
-- TABELA 4: SALUNO (Dados do Aluno)
-- ============================================================================
-- Descrição: Registro cadastral do aluno

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- RA (varchar)                      → Registro Acadêmico (PK)
-- CODPESSOA (int)                   → FK → PPESSOA (dados pessoais)
-- CODTIPOCURSO (smallint)           → FK → STIPOCURSO (polo de ingresso)
-- ANOINGRESSO (varchar)             → Ano em que ingressou


-- ============================================================================
-- TABELA 5: SHABILITACAOFILIAL (Curso + Polo + Período)
-- ============================================================================
-- Descrição: Oferta de um curso em um polo específico

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- IDHABILITACAOFILIAL (int)         → ID único (PK)
-- CODCURSO (varchar)                → FK → SCURSO (código do curso)
-- CODHABILITACAO (varchar)          → Tipo de habilitação (Bacharelado, etc)
-- CODFILIAL (smallint)              → Filial/polo
-- CODTIPOCURSO (smallint)           → FK → STIPOCURSO (tipo/polo)
-- CODTURNO (int)                    → FK → STURNO (turno do curso)


-- ============================================================================
-- TABELA 6: SCURSO (Curso)
-- ============================================================================
-- Descrição: Cadastro de cursos

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- CODCURSO (varchar)                → ID do curso (PK)
-- NOME (varchar)                    → Nome do curso
-- COMPLEMENTO (varchar)             → Complemento (modalidade)
-- CODCURINEP (varchar)              → Código MEC/INEP
-- CODTIPOCURSO (smallint)           → FK → STIPOCURSO


-- ============================================================================
-- TABELA 7: STIPOCURSO (Tipo de Curso / Polo)
-- ============================================================================
-- Descrição: Define tipo/polo/nível de ensino

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- CODTIPOCURSO (smallint)           → ID do tipo (PK)
-- NOME (varchar)                    → Nome do polo/tipo (ex: "UNINTA Sobral")


-- ============================================================================
-- TABELA 8: PPESSOA (Dados Pessoais)
-- ============================================================================
-- Descrição: Cadastro de pessoas (alunos, professores, funcionários)

-- Colunas principais:
-- CODIGO (int)                      → ID da pessoa (PK)
-- NOME (varchar)                    → Nome completo
-- NOMESOCIAL (varchar)              → Nome social
-- CPF (varchar)                     → CPF
-- EMAIL (varchar)                   → E-mail
-- CODUSUARIO (varchar)              → FK → GUSUARIO


-- ============================================================================
-- TABELA 9: HSOLICITACAO (Texto da Solicitação)
-- ============================================================================
-- Descrição: Texto livre da solicitação do atendimento

-- Colunas principais:
-- CODCOLIGADA (smallint)            → Coligada
-- CODATENDIMENTO (int)              → ID do atendimento (FK → HATENDIMENTOBASE)
-- CODLOCAL (int)                    → Local
-- TEXTOSOLICITACAO (text)           → Descrição/motivo da solicitação


-- ============================================================================
-- RELACIONAMENTOS (JOINs utilizados)
-- ============================================================================

/*
   HATENDIMENTOBASE
        ├─ JOIN SATENDIMENTO
        │   ├─ JOIN SALUNO
        │   │   ├─ JOIN SHABILITACAOFILIAL
        │   │   │   ├─ JOIN SCURSO
        │   │   │   └─ JOIN STIPOCURSO
        │   │   └─ JOIN PPESSOA
        │   └─ JOIN SPLETIVO (período letivo)
        ├─ LEFT JOIN HHISTORICOETAPASATENDIMENTO
        │   └─ (histórico de quem processou)
        └─ LEFT JOIN HSOLICITACAO
            └─ (texto da solicitação)
*/


-- ============================================================================
-- VALORES DE EXEMPLO
-- ============================================================================

-- CODCOLIGADA = 1
--   → UNINTA (sempre usar 1)

-- CODTIPOATENDIMENTO = 663
--   → Rematrícula - UNINTA SOBRAL
--   Outros tipos comuns:
--   180/58  → Trancamento de Matrícula
--   181/59  → Desistência Formalizada
--   183/49  → Transferência Externa
--   182/60  → Matrícula Institucional
--   82      → Transferência Interna

-- STIPOCURSO.CODTIPOCURSO
--   1   → UNINTA Sobral (presencial)
--   195 → F5
--   196 → UNINTA Itapipoca
--   281 → FIED
--   285 → UNINTA Tianguá
--   345 → UNINTA Fortaleza
--   357 → UNINTA Gestão e Negócios Fortaleza
--   424 → UNINTA Umirim

-- SPLETIVO.CODPERLET (formato)
--   "2026.1"  → Primeiro semestre de 2026
--   "2026.2"  → Segundo semestre de 2026


-- ============================================================================
-- AUDITAR IA E AUDITORIA
-- ============================================================================

-- Se precisar rastrear QUEM alterou os dados (via auditoria TOTVS):

SELECT
    TOTVSAUDIT.HATENDIMENTOBASE.AUDITACTION,
    TOTVSAUDIT.HATENDIMENTOBASE.LOGUSER,
    TOTVSAUDIT.HATENDIMENTOBASE.RECMODIFIEDON,
    TOTVSAUDIT.HATENDIMENTOBASE.CODATENDIMENTO,
    TOTVSAUDIT.HATENDIMENTOBASE.CODSTATUS,
    TOTVSAUDIT.HATENDIMENTOBASE.FECHAMENTO
FROM TOTVSAUDIT.HATENDIMENTOBASE
WHERE TOTVSAUDIT.HATENDIMENTOBASE.CODCOLIGADA = 1
  AND TOTVSAUDIT.HATENDIMENTOBASE.CODTIPOATENDIMENTO = 663
  AND CAST(TOTVSAUDIT.HATENDIMENTOBASE.RECMODIFIEDON AS DATE) IN ('2026-07-12', '2026-07-13')
ORDER BY TOTVSAUDIT.HATENDIMENTOBASE.RECMODIFIEDON DESC;


/* ============================================================================
   RESUMO: Colunas Essenciais para o Ticket
   ============================================================================
   
   Para identificar atendimentos finalizados por engano:
   
   Usar: HATENDIMENTOBASE.CODATENDIMENTO
   Filter: CODTIPOATENDIMENTO = 663
   Filter: FECHAMENTO entre 12-13 julho
   Track: HHISTORICOETAPASATENDIMENTO.MUDANCADEETAPA
   Track: HHISTORICOETAPASATENDIMENTO.CODATENDENTEATUAL (quem processou)
   Return: RA (aluno) para validação
   
   ============================================================================ */
