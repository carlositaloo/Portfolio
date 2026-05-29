# Contexto: TOTVS RM Gestão Educacional — UNINTA

## Sistema

- **Banco de dados:** SQL Server — TOTVS RM Gestão Educacional
- **Instituição:** UNINTA — Centro Universitário INTA
- **Acesso:** **SOMENTE LEITURA** — nunca gerar `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE` ou qualquer DDL/DML de modificação
- **Servidor:** banco corporativo privado; toda query deve ser conservadora e sem efeito colateral
- **Servidor de consulta/verificação (LLM):** sempre usar `172.31.58.205` (banco de teste) ao conectar para explorar estrutura de tabelas, validar colunas ou testar queries — **nunca** conectar em `172.31.58.204` (produção)

---

## Regras Obrigatórias

### Segurança
- **Proibido absolutamente:** `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`, `EXEC`, `sp_`, `xp_`
- Nunca sugerir operações que bloqueiem tabelas ou gerem locks
- Nunca usar `SELECT INTO` (cria tabela)
- Usar sempre `TOP n` para consultas exploratórias/testes

### Performance e Locks
- **Sempre** usar `WITH (NOLOCK)` em **todas** as tabelas de usuário referenciadas
  - Correto: `FROM SALUNO WITH (NOLOCK)`
  - Correto (JOIN): `JOIN PPESSOA WITH (NOLOCK) ON ...`
  - **Não aplicar** em views de sistema (`INFORMATION_SCHEMA`, `sys.*`)
- Sempre filtrar por `CODCOLIGADA` nos joins para evitar produto cartesiano entre coligadas
- Preferir filtro por `CODCOLIGADA = 1` como padrão (coligada principal da UNINTA)

### Qualidade do Código
- Nunca usar `SELECT *` em consultas finais — listar colunas explicitamente
- Palavras-chave SQL sempre em **MAIÚSCULAS** (`SELECT`, `FROM`, `WHERE`, `JOIN`, `ON`, etc.)
- Sempre comentar o que a consulta faz (`-- comentário` ou `/* bloco */`)
- **Proibido usar aliases (apelidos) de tabela** — sempre referenciar o nome completo original da tabela (ex: `HCLIENTEATENDIMENTO.RAALUNO`, nunca `HCA.RAALUNO`)
- Sem linhas em branco dentro de blocos `FROM`/`JOIN` contíguos
- Adicionar `;` ao final de cada instrução
- Usar `CONVERT(DECIMAL(18,2), ...)` para cálculos de porcentagem e valores monetários
- Usar `ISNULL(campo, default)` ou `COALESCE(a, b, c)` em campos que podem ser `NULL`
- Usar `LTRIM(RTRIM(campo))` para campos de texto que podem ter espaços

### Parâmetros TOTVS RM
- Parâmetros de relatório: `:NOME` (valor único) ou `:$NOME` (lista/combo — ex.: multi-seleção)
- Exemplo: `WHERE SPLETIVO.CODPERLET = :CODPERLET`
- Exemplo combo: `WHERE SCURSO.CODTIPOCURSO = :$CODTIPOCURSO`

---

## Glossário de Tabelas

### Pessoas e Usuários

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `PPESSOA` | Todas as pessoas cadastradas (alunos, professores, colaboradores, qualquer pessoa) | `CODIGO` |
| `GUSUARIO` | Usuários do sistema TOTVS | `CODUSUARIO` |
| `GUSRPERFIL` | Perfis de acesso atribuídos a usuários. Ex: `fun_web` (portal RH), `fun_web_pto` (ponto eletrônico). | `CODUSUARIO, CODPERFIL` |
| `PFUNC` | Colaboradores / funcionários da instituição | `CODCOLIGADA, CHAPA` |
| `PFUNCAO` | Cargos e funções dos colaboradores | `CODCOLIGADA, CODIGO` |
| `PSECAO` | Seções / departamentos dos colaboradores | `CODCOLIGADA, CODIGO` |

> **Atenção:** `PPESSOA.CODIGO` = `SALUNO.CODPESSOA` = `SPROFESSOR.CODPESSOA` = `PFUNC.CODPESSOA`

### Alunos

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `SALUNO` | Alunos cadastrados. Campo `RA` é o identificador único do aluno. | `CODCOLIGADA, RA` |
| `SHABILITACAOALUNO` | Vínculo do aluno com um curso/habilitação/polo específico. Um aluno pode ter múltiplos vínculos (transferências, re-ingresso). | `CODCOLIGADA, RA, IDHABILITACAOFILIAL` |
| `SMATRICPL` | Matrícula do aluno em um período letivo dentro de uma habilitação. Status reflete situação no período. | `CODCOLIGADA, RA, IDHABILITACAOFILIAL, IDPERLET` |
| `SMATRICPLITEMCNT` | Itens de contrato vinculados à matrícula do período letivo (LEFT JOIN em consultas de matrícula). | `CODCOLIGADA, RA, IDHABILITACAOFILIAL, IDPERLET` |
| `SMATRICULA` | Matrícula do aluno em disciplinas. **Única tabela de matrícula em disciplinas nesta instalação** — `SMATRICDISC` não existe aqui. | `CODCOLIGADA, RA, IDTURMADISC` |

### Cursos, Grades e Disciplinas

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `SCURSO` | Cursos da instituição. Contém `CODCURINEP` (código MEC/INEP). | `CODCOLIGADA, CODCURSO` |
| `SHABILITACAO` | Habilitações de um curso (Ex: Bacharelado, Licenciatura). | `CODCOLIGADA, CODCURSO, CODHABILITACAO` |
| `SHABILITACAOFILIAL` | Oferta de curso por filial/polo. Liga curso ao polo (`CODTIPOCURSO`). | `CODCOLIGADA, IDHABILITACAOFILIAL` |
| `SGRADE` | Grades curriculares | `CODCOLIGADA, CODCURSO, CODHABILITACAO, CODGRADE` |
| `SDISCGRADE` | Disciplinas dentro de uma grade curricular. Liga disciplina à grade/habilitação/curso. | `CODCOLIGADA, CODCURSO, CODHABILITACAO, CODGRADE, CODDISC` |
| `SDISCIPLINA` | Disciplinas cadastradas | `CODCOLIGADA, CODDISC` |
| `STURMA` | Turmas | `CODCOLIGADA, CODTURMA` |
| `STURMADISC` | Oferta de disciplina em uma turma (período letivo + disciplina + turma). Chave de join com matrículas. | `CODCOLIGADA, IDTURMADISC` |
| `STURNO` | Turnos (Manhã, Tarde, Noite, EAD...) | `CODCOLIGADA, CODTURNO` |

### Períodos, Status e Tipos

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `SPLETIVO` | Períodos letivos (ex: `'2026.1'`). Campo `CODPERLET` é o código legível. | `CODCOLIGADA, IDPERLET` |
| `SSTATUS` | Tabela genérica de status compartilhada por matrículas, habilitações, disciplinas etc. | `CODCOLIGADA, CODSTATUS` |
| `STIPOCURSO` | Tipos de curso / Polos / Níveis de ensino. Distingue presencial, EAD, semipresencial. Também chamado de "nível de ensino" em contextos de professores e turmas. | `CODCOLIGADA, CODTIPOCURSO` |
| `STIPOINGRESSO` | Formas de ingresso (ENEM, Vestibular, Transferência Interna/Externa...) | `CODCOLIGADA, CODTIPOINGRESSO` |
| `STIPOMATRICULA` | Tipos de matrícula | `CODCOLIGADA, CODTIPOMAT` |

### Professores

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `SPROFESSOR` | Professores cadastrados | `CODCOLIGADA, CODPROF` |
| `SPROFESSORTURMA` | Vínculo professor ↔ turma-disciplina | `CODCOLIGADA, CODPROF, IDTURMADISC` |

### Atendimentos / Requerimentos Acadêmicos

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `HATENDIMENTOBASE` | Cabeçalho dos atendimentos/requerimentos | `CODCOLIGADA, CODATENDIMENTO, CODLOCAL` |
| `SATENDIMENTO` | Dados acadêmicos do atendimento (RA, curso, período) | `CODCOLIGADA, CODATENDIMENTO, CODLOCAL` |
| `HCLIENTEATENDIMENTO` | Vínculo cliente/aluno ↔ atendimento. Campo `RAALUNO` liga ao RA do aluno solicitante. | `CODCOLIGADA, CODATENDIMENTO, CODLOCAL` |
| `HSOLICITACAO` | Texto livre da solicitação do atendimento | `CODCOLIGADA, CODATENDIMENTO, CODLOCAL` |
| `HPARAMATENDIMENTO` | Parâmetros/respostas preenchidas no atendimento | `CODCOLIGADA, CODATENDIMENTO, CODPARAMETRO` |

### Permissões e Polos

| Tabela | Descrição | Chave Principal |
|--------|-----------|-----------------|
| `SUSUARIOFILIAL` | Permissões do usuário por filial/polo. Para verificar se usuário tem acesso a um polo. | `CODCOLIGADA, CODUSUARIO, CODTIPOCURSO, CODFILIAL` |
| `ZMDPOLOS` | Dados adicionais dos polos: código INEP, tipo de ensino, polo digital | `CODCOLIGADA, CODPOLO` |

### Metadados do Sistema

| Tabela | Descrição |
|--------|-----------|
| `GLINKSREL` | Relacionamentos entre tabelas do TOTVS (use para descobrir joins desconhecidos). Colunas: `MASTERTABLE`, `CHILDTABLE` |

### Auditoria (TOTVSAUDIT)

| Tabela | Descrição |
|--------|----------|
| `TOTVSAUDIT.<tabela>` | Schema de auditoria. Contém cópia de **cada versão** dos registros antes/depois de alterações e registros excluídos. Mesmo nome da tabela original, prefixado com o schema `TOTVSAUDIT.` |

#### Colunas exclusivas do schema TOTVSAUDIT (presentes em todas as tabelas auditadas)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `LOGID` | bigint | Identificador único do evento de log |
| `PARENTLOGID` | bigint | Log pai — agrupa eventos relacionados de uma mesma operação |
| `AUDITID` | bigint | **Chave para comparar antes/depois** — mesmo `AUDITID` liga `AUDITACTION='O'` (antes) com `AUDITACTION='U'` (depois) |
| `AUDITACTION` | char(1) | **`'I'`** = inserção · **`'O'`** = valor antes da alteração · **`'U'`** = valor depois da alteração · **`'D'`** = exclusão |
| `LOGAPP` | varchar(128) | Aplicação que gerou a alteração (ex: `RM.exe`, `RMSErv`) |
| `LOGUSER` | varchar(128) | Usuário TOTVS que realizou a operação |
| `RECMODIFIEDON` | datetime | Data/hora da alteração |

> As demais colunas são espelho da tabela original com os valores no momento do evento.

#### Padrões de uso

```sql
-- 1. Ver TODO o histórico de uma chapa em ZMDFOLGAS (incluindo linhas excluídas)
SELECT TOTVSAUDIT.ZMDFOLGAS.AUDITACTION,
       TOTVSAUDIT.ZMDFOLGAS.LOGUSER,
       TOTVSAUDIT.ZMDFOLGAS.RECMODIFIEDON,
       TOTVSAUDIT.ZMDFOLGAS.IDFOLGAS,
       TOTVSAUDIT.ZMDFOLGAS.DATASERVICO,
       TOTVSAUDIT.ZMDFOLGAS.QTD,
       TOTVSAUDIT.ZMDFOLGAS.CREDITODEBITO
FROM TOTVSAUDIT.ZMDFOLGAS
WHERE TOTVSAUDIT.ZMDFOLGAS.CHAPA = '04788'
ORDER BY TOTVSAUDIT.ZMDFOLGAS.RECMODIFIEDON DESC;

-- 2. Linhas excluídas de ZMDFOLGAS (não existem mais na tabela original)
SELECT TOTVSAUDIT.ZMDFOLGAS.LOGUSER,
       TOTVSAUDIT.ZMDFOLGAS.RECMODIFIEDON,
       TOTVSAUDIT.ZMDFOLGAS.IDFOLGAS,
       TOTVSAUDIT.ZMDFOLGAS.DATASERVICO,
       TOTVSAUDIT.ZMDFOLGAS.QTD,
       TOTVSAUDIT.ZMDFOLGAS.CREDITODEBITO,
       TOTVSAUDIT.ZMDFOLGAS.DESCRICAOSERVICO
FROM TOTVSAUDIT.ZMDFOLGAS
WHERE TOTVSAUDIT.ZMDFOLGAS.AUDITACTION = 'D'
  AND TOTVSAUDIT.ZMDFOLGAS.CHAPA       = '04788'
ORDER BY TOTVSAUDIT.ZMDFOLGAS.RECMODIFIEDON DESC;

-- 3. Comparar valor antes x depois de uma alteração (JOIN por AUDITID)
SELECT ANTES.RECMODIFIEDON                  AS DATA_ALTERACAO,
       ANTES.LOGUSER                        AS USUARIO,
       ANTES.QTD                            AS QTD_ANTES,
       DEPOIS.QTD                           AS QTD_DEPOIS,
       ANTES.CREDITODEBITO                  AS CD_ANTES,
       DEPOIS.CREDITODEBITO                 AS CD_DEPOIS,
       ANTES.DATASERVICO                    AS DATA_ANTES,
       DEPOIS.DATASERVICO                   AS DATA_DEPOIS
FROM TOTVSAUDIT.ZMDFOLGAS AS ANTES
JOIN TOTVSAUDIT.ZMDFOLGAS AS DEPOIS
    ON DEPOIS.AUDITID     = ANTES.AUDITID
   AND DEPOIS.AUDITACTION = 'U'
WHERE ANTES.AUDITACTION   = 'O'
  AND ANTES.CHAPA         = '04788'
ORDER BY ANTES.RECMODIFIEDON DESC;
```

> **TOTVSAUDIT não suporta `WITH (NOLOCK)`** — é um schema especial; omitir o hint nessas tabelas.

---

## Relacionamentos Principais (Diagrama)

```
PPESSOA.CODIGO
    ├── SALUNO.CODPESSOA
    │       └── SHABILITACAOALUNO (CODCOLIGADA + RA)
    │               └── SMATRICPL (CODCOLIGADA + RA + IDHABILITACAOFILIAL)
    │                       └── SPLETIVO (CODCOLIGADA + IDPERLET)
    │                       └── SSTATUS  (CODCOLIGADA + CODSTATUS)  ← status do período
    │               └── SHABILITACAOFILIAL (CODCOLIGADA + IDHABILITACAOFILIAL)
    │                       └── SCURSO       (CODCOLIGADA + CODCURSO)
    │                       └── STIPOCURSO   (CODCOLIGADA + CODTIPOCURSO)  ← polo
    │                               └── ZMDPOLOS (CODCOLIGADA + CODPOLO) [LEFT JOIN]
    │                       └── STURNO       (CODCOLIGADA + CODTURNO)
    │                       └── SHABILITACAO (CODCOLIGADA + CODCURSO + CODHABILITACAO)
    │                               └── SGRADE (CODCOLIGADA + CODCURSO + CODHABILITACAO + CODGRADE)
    │               └── SSTATUS  ← status da habilitação (SHABILITACAOALUNO.CODSTATUS)
    │
    ├── SPROFESSOR.CODPESSOA
    │       └── SPROFESSORTURMA (CODCOLIGADA + CODPROF)
    │               └── STURMADISC (CODCOLIGADA + IDTURMADISC)
    │                       └── SDISCIPLINA (CODCOLIGADA + CODDISC)
    │                       └── STURMA      (CODCOLIGADA + CODTURMA)
    │                       └── SPLETIVO    (CODCOLIGADA + IDPERLET)
    │                       └── SHABILITACAOFILIAL (CODCOLIGADA + IDHABILITACAOFILIAL)
    │
    └── PFUNC.CODPESSOA
            └── PFUNCAO  (CODCOLIGADA + CODFUNCAO)
            └── PSECAO   (CODCOLIGADA + CODSECAO)

STURMADISC.IDTURMADISC
    └── SMATRICULA  (CODCOLIGADA + RA + IDTURMADISC)  ← disciplinas do aluno (SMATRICDISC não existe nesta instalação!)
            └── SPLETIVO (CODCOLIGADA + IDPERLET)
            └── SHABILITACAOFILIAL (CODCOLIGADA + IDHABILITACAOFILIAL)
            └── SSTATUS (CODCOLIGADA + CODSTATUS)  ← status da disciplina

HATENDIMENTOBASE (CODCOLIGADA + CODATENDIMENTO + CODLOCAL)
    ├── SATENDIMENTO  ← dados acadêmicos
    ├── HSOLICITACAO  ← texto da solicitação
    └── HPARAMATENDIMENTO (CODCOLIGADA + CODATENDIMENTO + CODPARAMETRO)

GUSUARIO.CODUSUARIO = PPESSOA.CODUSUARIO
    └── GUSRPERFIL (CODUSUARIO + CODPERFIL)  ← perfis de acesso (fun_web, fun_web_pto)
SUSUARIOFILIAL (CODCOLIGADA + CODUSUARIO + CODTIPOCURSO + CODFILIAL) ← permissões por polo

HATENDIMENTOBASE (CODCOLIGADA + CODATENDIMENTO + CODLOCAL)
    └── HCLIENTEATENDIMENTO (CODCOLIGADA + CODATENDIMENTO + CODLOCAL)
            └── SALUNO (CODCOLIGADA + RAALUNO = RA)
```

---

## Valores de Domínio Conhecidos

### SSTATUS — Status de Matrícula no Período (`SMATRICPL`)
```
'MATRICULADO (PERIODO LETIVO)'
'PENDENTE PAGAMENTO'
'PENDENTE ADITAMENTO'
'PENDENTE PAGAMENTO/ADITAMENTO'
'PENDENTE PAGAMENTO/FINANC'
'PENDENTE PAGAMENTO/MINUTA'
'TRANCADO'
```

### SSTATUS — Status de Habilitação (`SHABILITACAOALUNO`)
```
'ATIVO'
'GRADUADO(A)'
'CANCELADO'
'TRANCADO'
```

### SSTATUS — Status de Disciplina (`SMATRICULA`)
```
CODSTATUS = 1    → Aprovado
CODSTATUS = 10   → Reprovado por nota
CODSTATUS = 4319 → Reprovado por falta
```

### STIPOCURSO / Filtros de Polo

**Polos Presenciais:**
```
CODTIPOCURSO = 1   → UNINTA Sobral
CODTIPOCURSO = 195 → F5
CODTIPOCURSO = 196 → UNINTA Itapipoca
CODTIPOCURSO = 281 → FIED
CODTIPOCURSO = 285 → UNINTA Tianguá
CODTIPOCURSO = 345 → UNINTA Fortaleza
CODTIPOCURSO = 357 → UNINTA Gestão e Negócios Fortaleza
CODTIPOCURSO = 424 → UNINTA Umirim
```

```sql
-- Filtrar apenas polos presenciais:
SHABILITACAOFILIAL.CODTIPOCURSO IN (1, 195, 196, 281, 285, 345, 357, 424)

-- Polos EAD: STIPOCURSO.NOME LIKE 'POLO %'
-- Polos Semipresenciais: STIPOCURSO.NOME LIKE 'POLO %SEMI%'
-- CODTIPOCURSO = 4   → Presencial (EAD referência para buscar CODCURINEP)
-- CODTIPOCURSO = 323 → Semipresencial (referência para buscar CODCURINEP)
```

### ZMDPOLOS — Modalidade de Ensino
```
TIPOENSINO = 'P'                         → Presencial
TIPOENSINO = 'E' + POLODIGITAL = 'N'    → Flex (EAD)
TIPOENSINO = 'E' + POLODIGITAL = 'S'    → Digital (EAD)
TIPOENSINO = 'S'                         → Semipresencial
```

### HATENDIMENTOBASE — Tipos de Atendimento (`CODTIPOATENDIMENTO`)
```
180 / 58  → Trancamento de Matrícula
181 / 59  → Desistência Formalizada
183 / 49  → Transferência Externa
182 / 60  → Matrícula Institucional
82        → Transferência Interna
113       → Transferência Interna (variante)
686       → Criação de E-mail Institucional
```

### HPARAMATENDIMENTO — Parâmetros de Motivo
```
CODPARAMETRO IN (61, 63, 65, 67, 282) → campos de motivo nos atendimentos
```

### Mapeamento de Motivos por Tipo de Atendimento

> O campo `HPARAMATENDIMENTO.VALOR` tem significados **diferentes** conforme o tipo de atendimento:

**Transferência Interna (CODTIPOATENDIMENTO = 82):**
```
1 → Financeiro
2 → Trabalho
3 → Mudança de Domicilio
4 → Não se Identificou com o curso
5 → Descontentamento com o curso
```

**Demais tipos (180, 58, 181, 59, 183, 49, 182, 60):**
```
1 → Financeiro
2 → Saúde
3 → Trabalho
4 → Mudança de Domicílio
5 → Não se Identificou com o Curso
6 → Pessoal/Familiar
7 → Ensino Remoto/Pandemia
8 → Regularizar Situação Junto a IES
9 → Outros
```

### PFUNC — Situação do Colaborador (`CODSITUACAO`)
```
'A' → Ativo
'D' → Demitido
```

---

## Padrões Reutilizáveis

### Buscar aluno por CPF
```sql
-- Retorna RA e nome do aluno a partir do CPF
SELECT SALUNO.RA, PPESSOA.NOME, PPESSOA.CPF
FROM PPESSOA WITH (NOLOCK)
JOIN SALUNO WITH (NOLOCK)
    ON SALUNO.CODPESSOA = PPESSOA.CODIGO
WHERE PPESSOA.CPF = 'xxx'
  AND SALUNO.CODCOLIGADA = 1;
```

### Buscar pessoa por usuário do sistema
```sql
-- Retorna dados da pessoa vinculada a um CODUSUARIO
SELECT PPESSOA.CODUSUARIO, PPESSOA.NOME, PPESSOA.CPF, SALUNO.RA
FROM PPESSOA WITH (NOLOCK)
LEFT JOIN SALUNO WITH (NOLOCK)
    ON SALUNO.CODPESSOA = PPESSOA.CODIGO
   AND SALUNO.CODCOLIGADA = 1
WHERE PPESSOA.CODUSUARIO = 'xxx';
```

### Filtrar o período letivo mais recente do aluno
```sql
-- Subquery para pegar o IDPERLET mais atual dentro da habilitação
AND SMATRICPL.IDPERLET = (
    SELECT TOP 1 IDPERLET
    FROM SMATRICPL MP WITH (NOLOCK)
    WHERE MP.CODCOLIGADA         = SHABILITACAOALUNO.CODCOLIGADA
      AND MP.RA                  = SHABILITACAOALUNO.RA
      AND MP.IDHABILITACAOFILIAL = SHABILITACAOALUNO.IDHABILITACAOFILIAL
    ORDER BY MP.IDPERLET DESC
)
```

### Coluna POLO com código e indicador de permissão do usuário
```sql
CONCAT(
    STIPOCURSO.CODTIPOCURSO, ' - ',
    STIPOCURSO.NOME,
    CASE WHEN ZMDPOLOS.CODINEP IS NOT NULL
         THEN CONCAT(' (', ZMDPOLOS.CODINEP, ')') END,
    CASE WHEN NOT EXISTS (
            SELECT 1 FROM SUSUARIOFILIAL WITH (NOLOCK)
            WHERE SUSUARIOFILIAL.CODCOLIGADA  = SHABILITACAOFILIAL.CODCOLIGADA
              AND SUSUARIOFILIAL.CODTIPOCURSO = SHABILITACAOFILIAL.CODTIPOCURSO
              AND SUSUARIOFILIAL.CODFILIAL    = SHABILITACAOFILIAL.CODFILIAL
              AND SUSUARIOFILIAL.CODUSUARIO   = PPESSOA.CODUSUARIO
         ) THEN ' SEM PERMISSÃO'
    END
) AS POLO
```

### Joins ZMDPOLOS (polo) — sempre LEFT JOIN
```sql
JOIN STIPOCURSO WITH (NOLOCK)
    ON STIPOCURSO.CODCOLIGADA  = SHABILITACAOFILIAL.CODCOLIGADA
   AND STIPOCURSO.CODTIPOCURSO = SHABILITACAOFILIAL.CODTIPOCURSO
LEFT JOIN ZMDPOLOS WITH (NOLOCK)
    ON ZMDPOLOS.CODCOLIGADA = STIPOCURSO.CODCOLIGADA
   AND ZMDPOLOS.CODPOLO     = STIPOCURSO.CODTIPOCURSO
```

### Coluna CURSO com código INEP
```sql
CONCAT(
    SCURSO.NOME, ' (',
    (SELECT TOP 1 CODCURINEP
     FROM SCURSO A WITH (NOLOCK)
     WHERE A.CODCOLIGADA = SCURSO.CODCOLIGADA
       AND A.CODCURINEP IS NOT NULL
       AND (
           (STIPOCURSO.NOME LIKE 'POLO %SEMI%'
               AND A.COMPLEMENTO = SCURSO.COMPLEMENTO AND A.CODTIPOCURSO = 323)
           OR (STIPOCURSO.NOME LIKE 'POLO %' AND STIPOCURSO.NOME NOT LIKE '%SEMI%'
               AND A.COMPLEMENTO = SCURSO.COMPLEMENTO AND A.CODTIPOCURSO = 4)
           OR (STIPOCURSO.NOME NOT LIKE 'POLO %'
               AND A.CODCURSO = SCURSO.CODCURSO)
       )),
    ')'
) AS CURSO
```

### Colaborador sem duplicatas (múltiplos vínculos em PFUNC)
```sql
-- ROW_NUMBER prioriza situação Ativa ('A') quando há mais de um vínculo
LEFT JOIN (
    SELECT CODPESSOA, CODCOLIGADA, CODSECAO, CODFUNCAO, CODSITUACAO,
           ROW_NUMBER() OVER (
               PARTITION BY CODPESSOA
               ORDER BY CASE WHEN CODSITUACAO = 'A' THEN 0 ELSE 1 END
           ) AS RN
    FROM PFUNC WITH (NOLOCK)
    WHERE CODCOLIGADA = 1
) AS PFUNC_PRINCIPAL
    ON PFUNC_PRINCIPAL.CODPESSOA = PPESSOA.CODIGO
   AND PFUNC_PRINCIPAL.RN = 1
```

### Modalidade de ensino a partir de ZMDPOLOS
```sql
CASE
    WHEN ZMDPOLOS.TIPOENSINO = 'P'                                         THEN 'Presencial'
    WHEN ZMDPOLOS.TIPOENSINO = 'E' AND ISNULL(ZMDPOLOS.POLODIGITAL,'N')='N' THEN 'Flex'
    WHEN ZMDPOLOS.TIPOENSINO = 'E' AND ISNULL(ZMDPOLOS.POLODIGITAL,'N')='S' THEN 'Digital'
    WHEN ZMDPOLOS.TIPOENSINO = 'S'                                          THEN 'Semipresencial'
END AS MODALIDADE
```

---

## Colunas das Tabelas Principais

> Apenas colunas relevantes para JOINs, filtros e SELECT. Colunas de auditoria (LOGID, RECCREATEDBY, etc.) omitidas.

### PPESSOA
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODIGO` | int | **PK** — usado como FK em outras tabelas |
| `NOME` | varchar | Nome completo |
| `NOMESOCIAL` | varchar | Nome social (priorizar em exibição) |
| `CPF` | varchar | CPF sem formatação |
| `EMAIL` | varchar | E-mail principal |
| `EMAILPESSOAL` | varchar | E-mail pessoal secundário |
| `CODUSUARIO` | varchar | FK → GUSUARIO |
| `SEXO` | varchar | 'M' / 'F' |
| `DTNASCIMENTO` | datetime | Data de nascimento |
| `FALECIDO` | int | 1 = falecido |

### SALUNO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `RA` | varchar | **PK** — Registro do Aluno |
| `CODPESSOA` | int | FK → PPESSOA.CODIGO |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO (polo de ingresso) |
| `ANOINGRESSO` | varchar | Ano de ingresso |

### SHABILITACAOALUNO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `RA` | varchar | **PK** |
| `IDHABILITACAOFILIAL` | int | **PK** — FK → SHABILITACAOFILIAL |
| `CODSTATUS` | int | FK → SSTATUS (status da habilitação: ATIVO, CANCELADO…) |
| `DTINGRESSO` | datetime | Data de ingresso no curso |
| `DTCOLACAOGRAU` | datetime | Data de colação de grau |
| `CODTIPOINGRESSO` | smallint | FK → STIPOINGRESSO (ENEM, Vestibular…) |
| `IDHABILITACAOFILIALORIGEM` | int | FK → SHABILITACAOFILIAL (habilitação de origem em caso de transferência interna) |
| `CR` | numeric | Coeficiente de rendimento |
| `MEDIAGLOBAL` | numeric | Média global |

### SHABILITACAOFILIAL
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `IDHABILITACAOFILIAL` | int | **PK** |
| `CODFILIAL` | smallint | Filial/polo |
| `CODCURSO` | varchar | FK → SCURSO |
| `CODHABILITACAO` | varchar | FK → SHABILITACAO |
| `CODGRADE` | varchar | FK → SGRADE |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO (polo) |
| `CODTURNO` | int | FK → STURNO |
| `ATIVO` | varchar | 'S' = ativo |
| `OFERTAATIVA` | varchar | 'S' = oferta ativa |

### SCURSO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODCURSO` | varchar | **PK** |
| `NOME` | varchar | Nome do curso |
| `COMPLEMENTO` | varchar | Complemento/modalidade |
| `CODCURINEP` | varchar | Código MEC/INEP |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |

### SPLETIVO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `IDPERLET` | int | **PK** — chave numérica interna |
| `CODPERLET` | varchar | Código legível ex: `'2026.1'` |
| `DESCRICAO` | varchar | Descrição do período |
| `DTINICIO` | datetime | Início do período |
| `DTFIM` | datetime | Fim do período |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |
| `ENCERRADO` | varchar | 'S' = encerrado |

### SMATRICPL
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `RA` | varchar | **PK** |
| `IDHABILITACAOFILIAL` | int | **PK** |
| `IDPERLET` | int | **PK** |
| `CODSTATUS` | int | FK → SSTATUS (status no período) |
| `CODSTATUSRES` | int | FK → SSTATUS (status de resultado do período, quando houver) |
| `CODFILIAL` | smallint | Filial da matrícula |
| `CODTIPOMAT` | smallint | FK → STIPOMATRICULA (tipo de matrícula) |
| `DTMATRICULA` | datetime | Data de matrícula |
| `PERIODO` | int | Semestre dentro do curso (1, 2, 3…) |
| `CODTURMA` | varchar | Turma do aluno no período |

### SMATRICULA
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `RA` | varchar | **PK** |
| `IDTURMADISC` | int | **PK** — FK → STURMADISC |
| `CODSTATUS` | int | FK → SSTATUS (1=Aprovado, 10=Reprovado, 4319=Repr.Falta) |
| `IDPERLET` | int | FK → SPLETIVO |
| `IDHABILITACAOFILIAL` | int | FK → SHABILITACAOFILIAL |
| `TIPOMAT` | smallint | Tipo de matrícula |

### STURMADISC
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `IDTURMADISC` | int | **PK** |
| `CODTURMA` | varchar | FK → STURMA |
| `IDPERLET` | int | FK → SPLETIVO |
| `CODDISC` | varchar | FK → SDISCIPLINA |
| `IDHABILITACAOFILIAL` | int | FK → SHABILITACAOFILIAL |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |
| `CODTURNO` | int | FK → STURNO |
| `CODFILIAL` | smallint | Filial da turma-disciplina |
| `TIPO` | varchar | Modalidade da oferta: `'P'`=Presencial, `'D'`=Digital, `'E'`=EAD, `'S'`=Semipresencial |
| `MAXALUNOS` | int | Vagas máximas |
| `NOME` | varchar | Nome/código da turma-disciplina |

### SDISCIPLINA
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODDISC` | varchar | **PK** |
| `NOME` | varchar | Nome da disciplina |
| `CH` | numeric | Carga horária total |
| `NUMCREDITOS` | numeric | Número de créditos |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |

### STURMA
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODTURMA` | varchar | **PK** |
| `IDPERLET` | int | **PK** |
| `IDHABILITACAOFILIAL` | int | FK → SHABILITACAOFILIAL |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |
| `CODFILIAL` | smallint | Filial da turma |
| `MAXALUNOS` | int | Vagas máximas |
| `NOME` | varchar | Nome da turma |

### STURNO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODTURNO` | int | **PK** |
| `NOME` | varchar | Nome do turno |
| `TIPO` | varchar | Tipo (M=Manhã, T=Tarde, N=Noite, etc.) |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |

### SPROFESSOR
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODPROF` | varchar | **PK** |
| `CODPESSOA` | int | FK → PPESSOA.CODIGO |
| `CHAPA` | varchar | FK → PFUNC.CHAPA |

### SPROFESSORTURMA
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODPROF` | varchar | **PK** — FK → SPROFESSOR |
| `IDTURMADISC` | int | **PK** — FK → STURMADISC |
| `DTINICIO` | datetime | Início da atuação |
| `DTFIM` | datetime | Fim da atuação |
| `TIPOPROF` | varchar | Tipo de professor (regente, substituto…) |

### SSTATUS
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODSTATUS` | int | **PK** |
| `DESCRICAO` | varchar | Texto legível do status |
| `CODTIPOCURSO` | smallint | FK → STIPOCURSO |

### STIPOCURSO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODTIPOCURSO` | smallint | **PK** — também é `CODPOLO` em ZMDPOLOS |
| `NOME` | varchar | Nome do polo/tipo de curso/nível de ensino |

### GUSUARIO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODUSUARIO` | varchar | **PK** — igual a PPESSOA.CODUSUARIO |
| `NOME` | varchar | Nome do usuário |
| `NOMESOCIAL` | varchar | Nome social |
| `EMAIL` | varchar | E-mail do usuário |
| `STATUS` | smallint | Status da conta |

### PFUNC
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CHAPA` | varchar | **PK** |
| `CODPESSOA` | int | FK → PPESSOA.CODIGO |
| `CODFUNCAO` | varchar | FK → PFUNCAO.CODIGO |
| `CODSECAO` | varchar | FK → PSECAO.CODIGO |
| `CODSITUACAO` | char | `'A'`=Ativo, `'D'`=Demitido |
| `DATAADMISSAO` | datetime | Data de admissão |
| `DATADEMISSAO` | datetime | Data de demissão |
| `NOME` | varchar | Nome no registro de RH |
| `CODFILIAL` | smallint | Filial do colaborador |

### PFUNCAO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODIGO` | varchar | **PK** |
| `NOME` | varchar | Nome do cargo/função |
| `CBO` | varchar | Código CBO |

### PSECAO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODIGO` | varchar | **PK** |
| `DESCRICAO` | varchar | Nome do departamento/seção |

### HATENDIMENTOBASE
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODATENDIMENTO` | int | **PK** |
| `CODLOCAL` | int | **PK** |
| `CODTIPOATENDIMENTO` | int | Tipo do requerimento (180/58=Trancamento, 181/59=Desistência…) |
| `ABERTURA` | datetime | Data/hora de abertura |
| `FECHAMENTO` | datetime | Data/hora de fechamento |
| `PRIORIDADE` | int | Prioridade do atendimento |
| `CODSTATUS` | varchar | Status do atendimento |

### SATENDIMENTO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODATENDIMENTO` | int | **PK** |
| `CODLOCAL` | int | **PK** |
| `RA` | varchar | Aluno solicitante |
| `CODPROF` | varchar | Professor relacionado (se houver) |
| `IDHABILITACAOFILIAL` | int | FK → SHABILITACAOFILIAL |
| `IDPERLET` | int | FK → SPLETIVO |
| `IDTURMADISC` | int | FK → STURMADISC (se for requerimento de disciplina) |

### HSOLICITACAO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODATENDIMENTO` | int | **PK** |
| `CODLOCAL` | int | **PK** |
| `TEXTOSOLICITACAO` | text | Texto livre da solicitação |

### HPARAMATENDIMENTO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODATENDIMENTO` | int | **PK** |
| `CODLOCAL` | int | **PK** |
| `CODPARAMETRO` | int | **PK** — código do parâmetro (61,63,65,67,282 = motivo) |
| `VALOR` | varchar | Valor em texto curto |
| `VALOR_INTEIRO` | int | Valor inteiro |
| `VALOR_REAL` | numeric | Valor numérico |
| `VALOR_DATA` | datetime | Valor data |
| `VALOR_TEXTO` | text | Valor texto longo |

### SUSUARIOFILIAL
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODUSUARIO` | varchar | **PK** — FK → GUSUARIO |
| `CODTIPOCURSO` | smallint | **PK** — FK → STIPOCURSO |
| `CODFILIAL` | smallint | **PK** |
| `ACESSO` | varchar | `'S'` = com acesso ao polo |

### ZMDPOLOS
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | int | **PK** |
| `CODPOLO` | int | **PK** — equivale a `STIPOCURSO.CODTIPOCURSO` |
| `CODFILIAL` | int | Filial do polo |
| `CODINEP` | int | Código INEP do polo |
| `TIPOENSINO` | varchar | `'P'`=Presencial, `'E'`=EAD, `'S'`=Semipresencial |
| `POLODIGITAL` | varchar | `'S'`=Digital (EAD), `'N'`=Flex (EAD) |
| `ATIVO` | bit | 1 = polo ativo |
| `NOMECOORDENADOR` | varchar | Nome do coordenador de polo |
| `ENDERECO` | varchar | Endereço do polo |
| `CIDADE` | varchar | Cidade |
| `ESTADO` | varchar | Estado |

---

## Mapa Completo de Módulos do TOTVS RM

> O banco possui **8.379 tabelas**. As tabelas seguem prefixos que identificam o módulo TOTVS RM.
> Abaixo, a visão geral de **todos** os módulos, seguida de detalhamento dos mais relevantes.

| Prefixo | Módulo | Tabelas | Descrição |
|---------|--------|---------|-----------|
| `S*` | **Educacional (SGE)** | 2.643 | Módulo principal — alunos, cursos, matrículas, notas, frequência, bolsas, contratos, estágio, TCC, processo seletivo. Inclui sub-módulos `SPS*` (Processo Seletivo), `SZ*` (TOTVS Saúde — 1.651 tabelas) e `SPROJ*` (Pesquisa/Extensão). |
| `V*` | Views | 900 | Views de sistema e relatórios — projeções de leitura |
| `X*` | Customizações/Extensões | 778 | Tabelas de extensão do sistema — empreendimentos, contratos de locação, vendas imobiliárias |
| `P*` | **Pessoas / Folha (RH)** | 558 | Colaboradores, folha de pagamento, cargos, seções, benefícios, orçamento de pessoal |
| `T*` | Suprimentos / Compras | 467 | Produtos, movimentações, notas fiscais, almoxarifado, licitações |
| `M*` | Gestão de Projetos | 384 | Projetos, tarefas, contratos, transferências, medições |
| `G*` | **Globais / Sistema** | 363 | Coligadas, filiais, usuários, fórmulas, centros de custo, moedas, municípios, perfis |
| `D*` | Gestão Fiscal | 313 | Tributos, CFOP, naturezas, LAF, guias, obrigações acessórias |
| `F*` | **Financeiro** | 276 | Clientes/fornecedores (CFO), lançamentos, baixas, bancos, acordos, boletos, contratos |
| `E*` | Educacional Antigo | 258 | Módulo educacional legado — alunos, bolsas, mensalidades (versão anterior ao SGE) |
| `H*` | **Atendimento / Helpdesk** | 223 | Atendimentos, atendentes, tipos, tarefas, prospects, campanhas |
| `K*` | Planejamento e Produção | 193 | Ordens de produção, estrutura de produto, equipamentos, postos |
| `A*` | Ponto Eletrônico | 172 | Frequência de colaboradores, horários, ocorrências, jornadas |
| `C*` | Contabilidade Gerencial | 145 | Plano de contas, lançamentos contábeis, gerências, partidas, lotes |
| `I*` | Patrimônio | 133 | Bens patrimoniais, cálculo de depreciação, localizações, transferências |
| `O*` | Manutenção de Ativos | 117 | Objetos de oficina, ordens de serviço, indicadores, mão de obra |
| `L*` | **Biblioteca** | 108 | Publicações, exemplares, empréstimos, autores, editoras, reservas, periódicos |
| `U*` | Universidade (legado) | 99 | Módulo universitário antigo — cursos, grades, notas, contextos |
| `Z*` | **Customizações UNINTA** | 89 | Tabelas customizadas da UNINTA — polos, bolsas EAD, contrato digital, edital, censo, monitoria |
| `N*` | Portal / Intranet | 65 | Localidades, fórum, enquetes, notícias, menus do portal |
| `B*` | Avaliação e Pesquisa | 45 | Provas, questões, gabaritos, objetos avaliados, áreas |
| `R*` | Relatórios | 20 | Tabelas auxiliares de relatórios |
| `J*` | Jobs / Processos | 14 | Processos agendados, jobs automáticos |
| `Q*` | Questionários | 13 | Questionários auxiliares |
| `W*` | Web | 3 | Tabelas do módulo web |

---

## Módulo L — Biblioteca (108 tabelas)

> Módulo de gestão de acervo bibliográfico. Integra-se com o sistema Pergamum via `SPESSOAPERGAMUM`, `SMULTAPERGAMUM`.

### Tabelas Principais

| Tabela | Descrição | Relacionamentos-Chave |
|--------|-----------|----------------------|
| `LPUBLIC` | **Publicações** — livros, periódicos, teses. Tabela central do módulo. | Pai de: LEXEMPLAR, LEMPRESTIMOS, LASSUNTOPUB, LITEMAUTOR, LPERIODICO, LRESERVA |
| `LEXEMPLAR` | **Exemplares** — cópias físicas de uma publicação | FK → LPUBLIC, LUNIDADE, LSITUACAOEXEMPLAR, LVOLUME |
| `LEMPRESTIMOS` | **Empréstimos** — registros de empréstimo/devolução de exemplares | FK → LEXEMPLAR, LPUBLIC, LUSUARIO, LRESERVA |
| `LUSUARIO` | **Usuários da biblioteca** — leitores cadastrados | Pai de: LEMPRESTIMOS, LRESERVA, LESTPESQUISA, LSUGESTAO |
| `LAUTOR` | **Autores** de publicações | Pai de: LAUTORART, LAUTOREXEMP, LITEMAUTOR |
| `LEDITORA` | **Editoras** de publicações | Pai de: LPUBLIC (via FK) |
| `LASSUNTO` | **Assuntos** — classificação temática | Pai de: LASSUNTOPUB, LASSUNTOEXEMP |
| `LRESERVA` | **Reservas** de exemplares por usuários | FK → LEXEMPLAR, LPUBLIC, LUSUARIO, LUNIDADE |
| `LPERIODICO` | **Periódicos** — revistas, jornais com fascículos | FK → LPUBLIC, LEXEMPLAR |
| `LFASCICULO` | **Fascículos** de periódicos | FK → LEXEMPLAR |
| `LUNIDADE` | **Unidades** — bibliotecas setoriais/filiais | Pai de: LEXEMPLAR, LRESERVA, LSERVICO |
| `LSITUACAOEXEMPLAR` | **Situação do exemplar** (disponível, emprestado, em restauro…) | FK → LEXEMPLAR |
| `LREGRAEMPRESTIMO` | **Regras de empréstimo** por tipo de usuário/grupo | FK → LGRUPOPUBLIC, LTIPOUSUARIO |
| `LTIPOUSUARIO` | **Tipos de usuário** da biblioteca (aluno, professor, externo…) | Pai de: LUSUARIO, LREGRAEMPRESTIMO |
| `LTIPOPUBLIC` | **Tipos de publicação** (livro, tese, periódico, DVD…) | Pai de: LPUBLIC |
| `LCATEGORIA` | **Categorias** de publicações | FK → LPUBLIC |
| `LFONTE` | **Fontes** de aquisição | FK → LPUBFONTE |
| `LSERVICO` | **Serviços** oferecidos pela biblioteca | FK → LUNIDADE |
| `LCOLECAOSERIE` | **Coleções/séries** de publicações | FK → LPUBLIC |
| `LIDIOMAS` | **Idiomas** das publicações | FK → LPUBLIC, LESTPESQUISA |

### Relacionamentos Biblioteca (Diagrama)

```
LPUBLIC (Publicação)
    ├── LEXEMPLAR (exemplares físicos)
    │       ├── LEMPRESTIMOS → LUSUARIO
    │       ├── LSITUACAOEXEMPLAR
    │       ├── LASSUNTOEXEMP → LASSUNTO
    │       ├── LAUTOREXEMP → LAUTOR
    │       ├── LFASCICULO
    │       ├── LVOLUME
    │       └── LUNIDADE (biblioteca setorial)
    ├── LASSUNTOPUB → LASSUNTO
    ├── LITEMAUTOR → LAUTOR → LAUTORFUNC → LFUNCAOAUTORITEM
    ├── LPERIODICO → LASSINATURAPER
    ├── LRESERVA → LUSUARIO + LUNIDADE
    ├── LEDITORA
    ├── LCATEGORIA
    ├── LTIPOPUBLIC
    ├── LCOLECAOSERIE
    ├── LIDIOMAPUBLIC → LIDIOMAS
    └── LPUBFONTE → LFONTE

LUSUARIO (Leitor)
    ├── LEMPRESTIMOS
    ├── LRESERVA
    ├── LSUGESTAO
    ├── LESTPESQUISA
    ├── LTIPOUSUARIO → LREGRAEMPRESTIMO → LGRUPOPUBLIC
    └── LUSUUNI → LUNIDADE
```

### Integração Pergamum (Biblioteca)

| Tabela | Descrição |
|--------|-----------|
| `SPESSOAPERGAMUM` | Vínculo pessoa TOTVS ↔ usuário Pergamum |
| `SMULTAPERGAMUM` | Multas importadas do Pergamum |
| `SUNIDADEBIBLIPERGAMUM` | Unidades bibliográficas do Pergamum |
| `SLIVRO` | Livros cadastrados no educacional |
| `SREGISTROLIVRO` | Registros de livros |
| `SCVPRODBIBLIOGRAFICA` | Produção bibliográfica (currículo) |

### Colunas Relevantes da Biblioteca

#### LUNIDADE
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODIGO` | int | **PK** — código da unidade bibliotecária |
| `UNIDADE` | varchar | Nome da biblioteca setorial |

#### LUSUARIO
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODIGO` | int | **PK** — código do leitor |
| `CODPESSOA` | int | FK → PPESSOA.CODIGO |

#### LEMPRESTIMOS
| Coluna | Tipo | Observação |
|--------|------|------------|
| `CODCOLIGADA` | smallint | **PK** |
| `CODCLIENTE` | int | FK → LUSUARIO.CODIGO (leitor) |
| `CODUNIDADE` | int | FK → LUNIDADE.CODIGO (biblioteca) |
| `VALORMULTA` | numeric | Valor da multa (quando > 0, há pendência) |

---

## Tabelas Educacionais Adicionais (S*)

> Tabelas do módulo educacional que complementam o glossário principal. Agrupadas por funcionalidade.

### Notas e Frequência

| Tabela | Descrição |
|--------|-----------|
| `SNOTAS` | Notas lançadas por etapa/disciplina |
| `SNOTAETAPA` | Notas por etapa avaliativa |
| `SNOTAETAPACOMENTARIO` | Comentários dos professores nas notas |
| `SNOTASCOMENTARIO` | Comentários gerais sobre notas |
| `SFREQUENCIA` | Registros de frequência/presença dos alunos |

### Bolsas e Descontos

| Tabela | Descrição |
|--------|-----------|
| `SBOLSA` | Tipos de bolsa cadastrados |
| `SBOLSAALUNO` | Bolsas concedidas a alunos |
| `SBOLSAFILIAL` | Bolsas por filial/polo |
| `SBOLSAPLETIVO` | Bolsas vigentes por período letivo |
| `SBOLSALAN` | Lançamentos financeiros de bolsa |
| `SBOLSACONT` | Bolsas vinculadas a contratos |
| `SBOLSADESCPONTUAL` | Descontos pontuais de bolsa |
| `SBOLSAREPASSE` | Repasses de bolsa (FIES, ProUni, etc.) |
| `SBOLSARAT` | Rateio de bolsas |
| `SBOLSARETROATIVACONTRATO` | Bolsa retroativa vinculada a contrato |
| `SBOLSAPT` | Bolsas por tipo (parâmetros) |

### Contratos Acadêmicos

| Tabela | Descrição |
|--------|-----------|
| `SCONTRATO` | Contratos acadêmicos dos alunos |
| `SCONTRATOCONT` | Dados financeiros do contrato |
| `SCONTRATOBOLSA` | Bolsas vinculadas ao contrato |
| `SCONTRATOFIADOR` | Fiadores do contrato |
| `SCONTRATOSERVICO` | Serviços do contrato |
| `SCONTRATOSERVICOCONT` | Valores dos serviços contratados |
| `SCONTRATOACESSOS` | Acessos vinculados ao contrato |
| `SCONTRATODESCPONTUAL` | Descontos pontuais no contrato |
| `SCONTRATOLOGCONT` | Log de alterações no contrato |

### Estágio

| Tabela | Descrição |
|--------|-----------|
| `SESTAGIOCONTRATO` | Contratos de estágio |
| `SESTAGIOORIENTADOR` | Orientadores de estágio |
| `SESTAGIOAVALALUNO` | Avaliação do aluno no estágio |
| `SESTAGIOAVALEMPRESA` | Avaliação da empresa concedente |
| `SESTAGIOBANCA` | Bancas de avaliação de estágio |
| `SESTAGIOHISTCONTRATO` | Histórico de alterações no contrato de estágio |
| `SESTAGIOPLANOATIVIDADE` | Plano de atividades do estágio |
| `SESTAGIOSOLICITACAO` | Solicitações de estágio |
| `SESTAGIODOCUMENTOS` | Documentos do estágio |
| `SESTAGIOAPOLICE` | Apólice de seguro do estágio |

### TCC — Trabalho de Conclusão de Curso

| Tabela | Descrição |
|--------|-----------|
| `STCC` | TCCs cadastrados |
| `STCCORIENTADOR` | Orientadores de TCC |
| `STCCBANCA` | Bancas de TCC |
| `STCCPARTICIPANTESBANCA` | Membros da banca |
| `STCCMATALUNO` | Matrícula do aluno em TCC |
| `STCCLINHAPESQUISA` | Linhas de pesquisa |
| `STCCLINHAPESQUISAPROFESSOR` | Professores por linha de pesquisa |
| `STCCACOMPANHAMENTO` | Acompanhamento/orientação do TCC |
| `STCCSTATUS` | Status possíveis do TCC |
| `STCCTIPO` | Tipos de TCC |
| `STCCPROFESSORPERLET` | Professores ativos por período letivo |

### Processo Seletivo (SPS*)

| Tabela | Descrição |
|--------|-----------|
| `SPSPROCESSOSELETIVO` | Processos seletivos (vestibular, ENEM, etc.) |
| `SPSAREAOFERTADA` | Cursos/áreas ofertadas no processo seletivo |
| `SPSINSCRICAOAREAOFERTADA` | Inscrições dos candidatos por área |
| `SPSUSUARIO` | Usuários do portal de inscrição |
| `SPSCLASSIFICACAOGERAL` | Classificação geral dos candidatos |
| `SPSLOCAL` | Locais de prova |
| `SPSLANCAMENTO` | Lançamentos financeiros da inscrição |
| `SPSPARAMETRO` | Parâmetros configuráveis do processo |
| `SPSCONTROLEVAGAS` | Controle de vagas por área |
| `SPSCAMPUS` | Campus do processo seletivo |
| `SPSCONCURSOBOLSA` | Concurso de bolsas vinculado ao PS |
| `SPSDOCUMENTOEXIGIDO` | Documentos exigidos para matrícula |
| `SPSDOCUMENTOENTREGUE` | Documentos entregues pelo candidato |

### Pesquisa e Extensão (SPROJ*)

| Tabela | Descrição |
|--------|-----------|
| `SPROJPROJETO` | Projetos de pesquisa/extensão |
| `SPROJEDITAL` | Editais de pesquisa |
| `SPROJBOLSISTA` | Bolsistas de projetos |
| `SPROJPESQUISADOR` | Pesquisadores vinculados |
| `SPROJPARTICIPANTES` | Participantes do projeto |
| `SPROJPARCERIA` | Parcerias institucionais |
| `SPROJFREQUENCIA` | Frequência dos bolsistas |
| `SPROJDESEMBOLSO` | Desembolsos financeiros |
| `SPROJPLANOTRABALHO` | Planos de trabalho |

### Coordenação e Gestão

| Tabela | Descrição |
|--------|-----------|
| `SCOORDENADOR` | Coordenadores de curso |
| `SCOORDENADORPART` | Participações do coordenador |
| `SCOORDENADORBANCA` | Coordenador em bancas |

### Ficha Médica / Saúde do Aluno

| Tabela | Descrição |
|--------|-----------|
| `SFICHAMEDICAPESSOA` | Ficha médica da pessoa |
| `SFICHAMEDICAMODELO` | Modelos de ficha médica |
| `SFICHAMEDICACAMPO` | Campos configuráveis da ficha |
| `SFICHAMEDICAPESSOACAMPO` | Valores preenchidos nos campos |
| `SFICHAMEDICASECAO` | Seções da ficha médica |

### TOTVS Saúde (SZ* — 1.651 tabelas)

> Sub-módulo de saúde/hospitalar com prefixo `SZ*`. Inclui: agenda médica/cirúrgica, prontuário eletrônico, prescrições, exames laboratoriais, internação, faturamento SUS, centro cirúrgico, enfermagem. **Não é módulo educacional** — faz parte do TOTVS Saúde integrado ao mesmo banco.

---

## Customizações UNINTA (Z* — 89 tabelas)

> Tabelas criadas especificamente para a UNINTA. Prefixo `ZMD` = customização UNINTA via RM Maker/Data.

### Tabelas Principais

| Tabela | Descrição |
|--------|-----------|
| `ZMDPOLOS` | **Dados dos polos** — código INEP, tipo ensino, polo digital, coordenador, endereço *(já documentada acima)* |
| `ZMDBOLSAEAD` | Bolsas específicas para EAD |
| `ZMDBOLSAEADCURSO` | Cursos elegíveis para bolsa EAD |
| `ZMDBOLSAEADPOLO` | Polos elegíveis para bolsa EAD |
| `ZMDBOLSAEADPLETIVO` | Períodos letivos da bolsa EAD |
| `ZMDBOLSAEADPLANOPGTO` | Planos de pagamento da bolsa EAD |
| `ZMDCONTRATODIGITAL` | Contratos digitais (assinatura eletrônica) |
| `ZMDEDITAL` | Editais acadêmicos |
| `ZMDEDITALDIRETORIA` | Diretorias vinculadas ao edital |
| `ZMDEDITALIES` | IES do edital |
| `ZMDEDITALMODALIDADE` | Modalidades do edital |
| `ZMDEDITALTIPO` | Tipos de edital |
| `ZMDDADOSCENSO` | Dados para o Censo da Educação Superior |
| `ZMDDADOSENADE` | Dados para o ENADE |
| `ZMDENADECURSOPLETIVO` | Cursos por período letivo para ENADE |
| `ZMDENADECLASS­IFICACAOALUNO` | Classificação dos alunos no ENADE |
| `ZMDCAPTADORESUNINTA` | Captadores/comerciais da UNINTA |
| `ZMDDIPLOMAEXTERNO` | Diplomas de outras instituições |
| `ZMDEQUIVALENCIA` | Tabela de equivalência de disciplinas |
| `ZMDFOLGAS` | Folgas de colaboradores/professores |
| `ZMDTIPOSERVICOFOLGAS` | Tipos de serviço para folgas |
| `ZMDFIESOFERTADEVAGAS` | Oferta de vagas FIES |
| `ZMDCONTRATOSFIES` | **Contratos FIES** — dados extraídos diariamente do SISFIES via bot. Tabela principal com dados do aluno, contrato e curso. | 
| `ZMDCONTRATOSFIESADITAMENTOS` | Aditamentos dos contratos FIES (semestres renovados/alterados) | 
| `ZMDCONTRATOSFIESVALORESFIN` | Valores financeiros por período letivo de cada contrato FIES |
| `ZMDINTERNATOMED` | Internato de Medicina |
| `ZMDLOCAISMED` | Locais de prática médica |
| `ZMDMODULOMED` | Módulos do curso de Medicina |
| `ZMDLOTACAOAULAPRATICA` | Lotação em aulas práticas |
| `ZMDAGENDAAULAPRATICA` | Agenda de aulas práticas |
| `ZMDAGENDAAULAPRATICAPROF` | Professores na agenda de aulas práticas |
| `ZMDMONITORIA` | Monitorias acadêmicas |
| `ZMDTUTORIAEAD` | Tutoria EAD |
| `ZMDNPSCAMPANHA` | Campanhas NPS (pesquisa de satisfação) |
| `ZMDNPSRESPOSTA` | Respostas NPS |
| `ZMDPESQUISAEXTENSAO` | Pesquisa e extensão |
| `ZMDPROJETO` | Projetos institucionais |
| `ZMDVACINAS` | Controle de vacinas (cursos de saúde) |
| `ZMDTESTEPROGRESSO` | Teste de progresso acadêmico |
| `ZMDGATEWAYPAG` | Gateway de pagamento |
| `ZMDRECEBEDORGATEWAY` | Recebedores do gateway |
| `ZMDHISTORICOVALORES` | Histórico de valores de mensalidades |
| `ZMDSERVICOPADRAO` | Serviços padrão |
| `ZMDRATEIOPOS` | Rateio financeiro pós-graduação |
| `ZMDRATEIOSEAD` | Rateio financeiro EAD |
| `ZMDRATEIOSCENTROCUSTO` | Rateio por centro de custo |
| `ZMDLIBERACAOFUNC` | Liberações de funcionalidades |
| `ZMDCHEQUES` | Controle de cheques |
| `ZMDSITUACAOCHEQUE` | Situações de cheque |

### FIES — Contratos (ZMD*)

> Tabelas populadas diariamente por bot de extração do SISFIES (portal do MEC). São metadados do sistema inseridos via automação — **não existem nas tabelas nativas do TOTVS RM**. A chave de ligação com alunos é via `CPFALUNO` → `PPESSOA.CPF`.

#### ZMDCONTRATOSFIES
| Coluna | Tipo | Observação |
|--------|------|------------|
| `ID` | int | **PK** — identificador interno |
| `NUMCONTRATO` | varchar(30) | Número do contrato FIES no SISFIES |
| `TIPOPROCESSO` | varchar(50) | Tipo do processo (ex: Renovação, Aditamento) |
| `DTCONTRATO` | datetime | Data de assinatura do contrato |
| `SITCONTRATO` | varchar(50) | Situação do contrato no SISFIES |
| `CPFALUNO` | varchar(14) | CPF do aluno — FK → `PPESSOA.CPF` |
| `NOMEALUNO` | varchar(150) | Nome do aluno conforme SISFIES |
| `CODFIES` | varchar(20) | Código FIES do aluno |
| `DTNASCIMENTOALUNO` | datetime | Data de nascimento do aluno |
| `RG` | varchar(20) | RG do aluno |
| `DATAEMISSAO` | datetime | Data de emissão do RG |
| `ORGAOEMISSOR` | varchar(100) | Órgão emissor do RG |
| `SEXO` | varchar(20) | Sexo do aluno |
| `ENDERECO` | varchar(255) | Endereço |
| `BAIRRO` | varchar(100) | Bairro |
| `CIDADE` | varchar(100) | Cidade |
| `UF` | varchar(2) | Estado |
| `CEP` | varchar(10) | CEP |
| `TELRESIDENCIAL` | varchar(20) | Telefone residencial |
| `TELCELULAR` | varchar(20) | Telefone celular |
| `EMAIL` | varchar(150) | E-mail |
| `QTDSEMESTREFIN` | int | Quantidade de semestres financiados |
| `PERIODOFINANCIADO` | varchar(50) | Período financiado (ex: `'2026.1'`) |
| `QTDSEMESTREREST` | int | Quantidade de semestres restantes |
| `VALORLIMITE` | float | Valor limite do financiamento |
| `PERCENTUALFIN` | float | Percentual financiado pelo FIES |
| `TIPOFIANCA` | varchar(50) | Tipo de fiança |
| `CNPJMANTE` | varchar(20) | CNPJ da mantenedora |
| `MANTENEDORA` | varchar(255) | Nome da mantenedora |
| `DTEXTRACAO` | datetime | Data/hora da extração do SISFIES |
| `CODCURSO` | int | Código do curso no FIES |
| `CURSO` | varchar(500) | Nome do curso conforme SISFIES |
| `TURNO` | varchar(15) | Turno do curso |
| `CODCAMPUS` | int | Código do campus no FIES |
| `SITUACAO` | varchar(15) | Situação atual do contrato |

#### ZMDCONTRATOSFIESADITAMENTOS
| Coluna | Tipo | Observação |
|--------|------|------------|
| `IDADITAMENTO` | int | **PK** — identificador do aditamento |
| `IDCONTRATO` | int | **FK** → `ZMDCONTRATOSFIES.ID` |
| `NUMCONTRATO` | varchar(30) | Número do contrato FIES |
| `SEMESTRE` | varchar(10) | Semestre do aditamento (ex: `'2026.1'`) |
| `FINALIDADE` | varchar(100) | Finalidade do aditamento |
| `SITUACAO` | varchar(100) | Situação do aditamento |
| `TIPO` | varchar(100) | Tipo do aditamento |
| `PROUNI` | varchar(50) | Indicador de vínculo ProUni |
| `DATAINCLUSAO` | datetime | Data de inclusão do aditamento |
| `DATACONCLUSAO` | datetime | Data de conclusão do aditamento |
| `AUDITORIA` | varchar(MAX) | JSON/texto com dados de auditoria do SISFIES |
| `DOCUMENTOS` | varchar(MAX) | JSON/texto com documentos anexados |
| `DATAEXTRACAO` | datetime | Data/hora da extração do SISFIES |

#### ZMDCONTRATOSFIESVALORESFIN
| Coluna | Tipo | Observação |
|--------|------|------------|
| `IDVALORFIN` | int | **PK** — identificador do valor financeiro |
| `IDCONTRATO` | int | **FK** → `ZMDCONTRATOSFIES.ID` |
| `NUMCONTRATO` | varchar(30) | Número do contrato FIES |
| `PERIODO` | varchar(10) | Período letivo (ex: `'2026.1'`) |
| `VALOR` | money | Valor financiado no período |
| `DATAEXTRACAO` | datetime | Data/hora da extração do SISFIES |

---

### ZMDFOLGAS — Folgas de Colaboradores/Professores

> Registros de folgas, serviços externos e compensações de horas de colaboradores e professores. A chave de ligação com colaboradores é via `CHAPA` → `PFUNC.CHAPA`.

#### ZMDFOLGAS
| Coluna | Tipo | Observação |
|--------|------|------------|
| `IDFOLGAS` | int | **PK** — identificador da folga |
| `CODCOLIGADA` | int | **PK** — FK → `GCOLIGADA` |
| `CHAPA` | varchar(16) | FK → `PFUNC.CHAPA` — colaborador/professor |
| `IDTIPOSERVICO` | int | FK → `ZMDTIPOSERVICOFOLGAS` — tipo do serviço |
| `DATASERVICO` | datetime | Data de realização do serviço/folga |
| `DATAVALIDADE` | datetime | Data de validade da folga (pode ser nula) |
| `DESCRICAOSERVICO` | varchar(256) | Descrição do serviço prestado |
| `TIPOFOLGA` | varchar(10) | Tipo da folga |
| `QTD` | int | Quantidade (horas ou dias) |
| `CREDITODEBITO` | char(1) | `'C'`=Crédito (adiciona folga), `'D'`=Débito (desconta folga) |
| `APLICACAO` | char(1) | Aplicação da folga |
| `LOCALSERVICO` | varchar(200) | Local onde o serviço foi realizado |
| `PROCESSOFLUIG` | int | Número do processo no Fluig (quando originado por workflow) |
| `OBSERVACAO` | varchar(256) | Observações adicionais |

---

### Tabelas de Auditoria e Log (Z*)

| Tabela | Descrição |
|--------|-----------|
| `ZAUDITCHANGES` | Alterações auditadas |
| `ZAUDITCONFIG` | Configuração de auditoria |
| `ZAUDITEXCEPTION` | Exceções da auditoria |
| `ZAUDITITEMS` | Itens auditados |
| `ZAUDITPENDCHANGES` | Alterações pendentes de auditoria |
| `ZAUDITSCHEMAEVENTS` | Eventos de alteração de schema |
| `ZLOG` | Log genérico |
| `ZLOGCAMPOS` | Campos do log |
| `ZLOGEXCECAO` | Exceções do log |
| `ZLOGPARAMS` | Parâmetros do log |

### Tabelas de Integração MEC (Z*)

| Tabela | Descrição |
|--------|-----------|
| `ZEALUNOSMEC` | Dados de alunos para MEC |
| `ZEPROFESMEC` | Dados de professores para MEC |
| `ZEPROFESTURMASMEC` | Turmas de professores para MEC |
| `ZETURMASMEC` | Turmas para MEC |
| `ZMECRELCURSOSETAPAS` | Relação cursos/etapas MEC |
| `ZMECRELDISCIPLINAS` | Relação disciplinas MEC |
| `ZMECRELESCOLARIDADE` | Relação escolaridade MEC |
| `ZMECRELNACIONALIDADES` | Relação nacionalidades MEC |
| `ZMECRELORGAOEMISSOR` | Relação órgãos emissores MEC |

---

## Módulo F — Financeiro (276 tabelas)

> Tabelas do módulo financeiro. Relevante para consultas de mensalidades, lançamentos e inadimplência.

| Tabela | Descrição | Referências Principais |
|--------|-----------|----------------------|
| `FCFO` | **Clientes/Fornecedores** — cadastro financeiro de pessoas jurídicas e físicas | 274 referências — tabela central do financeiro |
| `FLAN` | **Lançamentos financeiros** — contas a pagar e receber | FK → FCFO, FTDO, FCXA |
| `FLANBAIXA` | **Baixas** — registros de pagamento/recebimento | FK → FLAN |
| `FTDO` | **Tipos de documento** — boleto, nota fiscal, recibo, etc. | 62 referências |
| `FCXA` | **Caixas/Contas bancárias** | 51 referências |
| `FCONVENIO` | **Convênios** financeiros | FK → FCFO |
| `FCONTRATO` | **Contratos** financeiros | FK → FCFO |
| `FAPLFIN` | **Aplicações financeiras** | FK → FCXA |
| `FACORDO` | **Acordos** — renegociação de dívidas | FK → FLAN |
| `FBOLETO` | **Boletos** bancários | FK → FLAN |
| `FCFOCONTATO` | **Contatos** do cliente/fornecedor | FK → FCFO |
| `FIRRF` | **IRRF** — retenções de imposto de renda | FK → FLAN |
| `FLANCONTOLD` | **Lançamentos contabilizados** | FK → FLAN |
| `FLANHST` | **Histórico** de lançamentos | FK → FLAN |
| `FTIPOAPLFIN` | **Tipos de aplicação** financeira | 21 referências |
| `FSESSAOCAIXA` | **Sessões de caixa** | FK → FCXA |

---

## Módulo G — Globais / Sistema (363 tabelas)

> Tabelas compartilhadas por todos os módulos TOTVS RM.

| Tabela | Descrição | Referências |
|--------|-----------|-------------|
| `GCOLIGADA` | **Coligadas** — empresas do grupo. CODCOLIGADA = 1 é a UNINTA. | 1.301 referências — mais referenciada do banco |
| `GFILIAL` | **Filiais** — unidades da coligada | 363 referências |
| `GUSUARIO` | **Usuários** do sistema *(já documentada)* | 297 referências |
| `GFORMULA` | **Fórmulas** — cálculos configuráveis do sistema | 280 referências |
| `GCCUSTO` | **Centros de custo** | 231 referências |
| `GDEPTO` | **Departamentos** | 122 referências |
| `GMOEDA` | **Moedas** (BRL, USD, etc.) | 104 referências |
| `GETD` | **ETD** — escrituração de documentos | 81 referências |
| `GMUNICIPIO` | **Municípios** — tabela IBGE | 65 referências |
| `GPERFIL` | **Perfis** de acesso | 38 referências |
| `GIMAGEM` | **Imagens** — fotos, logos, anexos | 30 referências |
| `GBANCO` | **Bancos** — cadastro de instituições financeiras | 23 referências |
| `GCONSSQL` | **Consultas SQL** salvas no sistema | 23 referências |
| `GSISTEMA` | **Parâmetros do sistema** | 22 referências |
| `GPAIS` | **Países** | 19 referências |
| `GCALEND` | **Calendários** | 14 referências |

---

## Módulo P — Pessoas / Folha de Pagamento (558 tabelas)

> RH e folha. As tabelas `PPESSOA`, `PFUNC`, `PFUNCAO`, `PSECAO` já estão documentadas no glossário principal.

| Tabela | Descrição | Referências |
|--------|-----------|-------------|
| `PFUNC` | **Funcionários** *(já documentada)* | 348 referências |
| `PPESSOA` | **Pessoas** *(já documentada)* | 225 referências |
| `PEVENTO` | **Eventos da folha** — rubricas de proventos e descontos | 144 referências |
| `PSECAO` | **Seções/departamentos** *(já documentada)* | 133 referências |
| `PFUNCAO` | **Funções/cargos** *(já documentada)* | 98 referências |
| `PCCUSTO` | **Centro de custo** de RH | 41 referências |
| `PEXTERNO` | **Autônomos/externos** | 32 referências |
| `PORCAMENTO` | **Orçamento** de pessoal | 26 referências |
| `PFINANCEIRO` | **Financeiro** de RH — pagamentos, adiantamentos | 20 referências |
| `PFDEPEND` | **Dependentes** do funcionário | 18 referências |
| `PSINDIC` | **Sindicatos** | 18 referências |
| `PCARGO` | **Cargos** (cargo ≠ função) | 16 referências |
| `PENCARGO` | **Encargos** sociais (INSS, FGTS) | 12 referências |
| `PLANCFINANC` | **Lançamentos financeiros** de folha | 10 referências |

---

## Módulo H — Atendimento / Helpdesk (223 tabelas)

> Atendimentos, requerimentos e CRM. As tabelas `HATENDIMENTOBASE`, `HSOLICITACAO`, `HPARAMATENDIMENTO` já estão documentadas.

| Tabela | Descrição | Referências |
|--------|-----------|-------------|
| `HATENDENTE` | **Atendentes** — quem pode abrir/processar atendimentos | 84 referências |
| `HATENDIMENTOEXT` | **Atendimento estendido** — dados adicionais | 54 referências |
| `HTIPOATENDIMENTO` | **Tipos de atendimento** — categorias (trancamento, transferência, etc.) | 36 referências |
| `HTAREFA` | **Tarefas** vinculadas a atendimentos | 23 referências |
| `HATENDIMENTOBASE` | **Cabeçalho** *(já documentada)* | 21 referências |
| `HPROSPECT` | **Prospects** — leads do CRM | 18 referências |
| `HLOCALIDADE` | **Localidades** de atendimento | 15 referências |
| `HACAO` | **Ações** possíveis no atendimento | 13 referências |
| `HGRUPOATENDIMENTO` | **Grupos** de atendimento | 13 referências |
| `HCAMPANHA` | **Campanhas** de marketing/CRM | 12 referências |
| `HPRODUTO` | **Produtos/serviços** do helpdesk | 12 referências |
| `HPROCESSOS` | **Processos** automatizados de atendimento | 12 referências |

---

## Outros Módulos (resumo)

### Módulo T — Suprimentos / Compras (467 tabelas)
Tabelas-chave: `TPRODUTO` (produtos), `TMOV` (movimentações), `TITMMOV` (itens da movimentação), `TPRD` (almoxarifado), `TUND` (unidades de medida), `TTMV` (tipos de movimentação), `TLOC` (locais de estoque), `TCPG` (condições de pagamento), `TNUMSERIE` (números de série).

### Módulo C — Contabilidade Gerencial (145 tabelas)
Tabelas-chave: `CCONTA` (plano de contas), `CGERENCIA` (gerências), `CHISTP` (histórico padrão), `CLOTE` (lotes contábeis), `CPARTIDA` (partidas/lançamentos), `COPERACAO` (operações contábeis).

### Módulo D — Gestão Fiscal (313 tabelas)
Tabelas-chave: `DTRIBUTO` (tributos), `DCFOP` (CFOP), `DNATUREZA` (naturezas fiscais), `DLAF` (livro apuração fiscal), `DLAFHISTORICO` (histórico LAF), `DITEM` (itens fiscais), `DGUIAPERIODO` (guias/DARF por período).

### Módulo I — Patrimônio (133 tabelas)
Tabelas-chave: `IPATRIMONIO` (bens patrimoniais), `IBEM` (cadastro de bens), `ICALCULOPATRIMONIO` (cálculos de depreciação), `ILOCAL` (localização dos bens), `IALOCACAO` (alocação de bens).

### Módulo A — Ponto Eletrônico (172 tabelas)
Tabelas-chave: `APARFUN` (parâmetros por função), `AHORARIO` (horários), `ATIPOOCORRENCIA` (tipos de ocorrência), `APARCOL` (parâmetros da coligada).

### Módulo K — Planejamento e Produção (193 tabelas)
Tabelas-chave: `KATVORDEM` (atividades da ordem), `KESTRUTURA` (estrutura de produto), `KITEMORDEM` (itens da ordem), `KEQUIPAMENTO` (equipamentos), `KPOSTO` (postos de trabalho).

### Módulo M — Gestão de Projetos (384 tabelas)
Tabelas-chave: `MPRJ` (projetos), `MTAREFA` (tarefas), `MCNT` (contratos), `MTRF` (transferências), `MISM` (itens de serviço/material), `MCMP` (componentes).

### Módulo O — Manutenção de Ativos (117 tabelas)
Tabelas-chave: `OFOBJOFICINA` (objetos de oficina), `OFTIPOOBJ` (tipos de objeto), `OFORDEMSERVICO` (ordens de serviço), `OFMAOOBRA` (mão de obra), `OFATENDIMENTO` (atendimentos de manutenção).

### Módulo E — Educacional Antigo (258 tabelas)
Módulo legado anterior ao SGE atual. Tabelas-chave: `EALUNOS` (alunos), `EALUBOLSA` (bolsas), `EALUMENS` (mensalidades), `EATENDIMENTO` (atendimentos), `EATIVEXT` (atividades extracurriculares). **Usar apenas para consultas históricas; o módulo atual é o S*.**

### Módulo B — Avaliação e Pesquisa (45 tabelas)
Tabelas-chave: `BPROVA` (provas), `BQUESTAO` (questões), `BOPCAO` (opções de resposta), `BEXECPROVA` (execução de prova), `BHISTORICO` (histórico), `BMATERIA` (matérias), `BAREA` (áreas de avaliação).

### Módulo N — Portal / Intranet (65 tabelas)
Tabelas-chave: `NLOCALIDADE` (localidades), `NFORUM` (fórum), `NENQUETE` (enquetes), `NNOTICIA` (notícias), `NEMPREGO` (banco de empregos), `NMENU` (menus do portal).

### Módulo X — Customizações / Extensões (778 tabelas)
Tabelas de extensão (imobiliário/aluguéis): `XEMPREENDIMENTO` (empreendimentos), `XVENDA` (vendas), `XALGIMOVEL` (imóveis), `XALGCONTRATOLOC` (contratos de locação), `XSUBUNIDADE` (subunidades), `XUNIDADE` (unidades).

### Módulo U — Universidade Legado (99 tabelas)
Módulo universitário da versão anterior: `UCURSOS` (cursos), `UDEFGRADE` (definição de grade), `UCONCEITOETAPA` (conceitos por etapa), `UALUCURSO` (aluno-curso). **Usar apenas para consultas históricas; o módulo atual é o S*.**

---

## Descoberta de Estrutura (Consultas Auxiliares)

```sql
-- Relacionamentos de uma tabela (sempre verificar antes de criar joins)
SELECT MASTERTABLE, CHILDTABLE
FROM GLINKSREL WITH (NOLOCK)
WHERE MASTERTABLE = 'NOME_DA_TABELA'
   OR CHILDTABLE  = 'NOME_DA_TABELA'
ORDER BY MASTERTABLE, CHILDTABLE;

-- Colunas de uma tabela
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'NOME_DA_TABELA'
ORDER BY ORDINAL_POSITION;

-- Listar todas as tabelas do banco
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
```

---

## Repositório de Consultas de Referência

O arquivo [`SQL.sql`](../SQL.sql) contém o repositório central de consultas validadas e prontas para uso neste banco.
**Sempre consulte este arquivo antes de criar uma nova query** — verifique se já existe algo semelhante e use como base de estrutura, joins e padrões de filtro.

### Índice do SQL.sql

| Seção | Conteúdo |
|-------|----------|
| 1. LOOKUPS RÁPIDOS | Exploração de tabelas e relacionamentos (`GLINKSREL`, `INFORMATION_SCHEMA`) |
| 2. ALUNOS | Dados cadastrais, polo, curso, turno, modalidade, disciplinas por período |
| 3. MATRÍCULAS E PERÍODOS | Situação de matrícula por período letivo (`SMATRICPL`) |
| 4. EMAIL INSTITUCIONAL | Geração de sugestão de e-mail `@discentes.uninta.edu.br` |
| 5. PESSOAS E USUÁRIOS | Perfil completo: aluno, colaborador, cargo, permissões Portal RH |
| 6. PROFESSORES | Polos de atuação e disciplinas por professor |
| 7. ATENDIMENTOS | Requerimentos acadêmicos com motivo declarado |
| 8. DESEMPENHO ACADÊMICO | Percentuais de aprovação/reprovação por curso e período |
| 9. LISTAS AUXILIARES | Listas de valores para parâmetros de relatórios |
| 10. FORMULÁRIOS E VALIDAÇÕES | Validações para formulários do portal (ex: bloqueio de duplicidade) |
| 11. BIBLIOTECA | Devedores com multa por unidade bibliográfica |
| 12. AUDITORIA | Histórico de alterações via `TOTVSAUDIT` |

---

## O que NUNCA fazer

| Proibido | Motivo |
|----------|--------|
| `INSERT / UPDATE / DELETE` | Banco read-only — acesso corporativo sem permissão de escrita |
| `DROP / ALTER / CREATE` | Idem — DDL completamente proibido |
| `SELECT *` em consultas finais | Retorna colunas desnecessárias, pesado em tabelas largas |
| `JOIN` sem `CODCOLIGADA` | Gera produto cartesiano entre coligadas diferentes |
| `WITH (NOLOCK)` em `INFORMATION_SCHEMA` | Views de sistema não suportam hint de lock |
| `TOP` sem `ORDER BY` quando a ordem importa | Resultado não determinístico |
| Queries sem filtro nenhum em tabelas grandes (`PPESSOA`, `SMATRICPL`) | Pode impactar performance do servidor |
