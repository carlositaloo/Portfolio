/* ============================================================================
   GUIA DE USO: Filtro de Atendimentos 663 finalizados por engano
   Data: 13/07/2026
   ============================================================================ */

-- ============================================================================
-- PASSO 1: EXECUTAR A CONSULTA PRINCIPAL (OPÇÃO 1 - RECOMENDADA)
-- ============================================================================
-- A OPÇÃO 1 usa HHISTORICOETAPASATENDIMENTO para rastrear o histórico de quem
-- processou o atendimento. Esta é a forma mais segura de identificar quem
-- finalizou o atendimento e quando.

-- Execute: consulta_rematricula_663.sql (OPÇÃO 1)
-- Esta consulta retornará:
-- - CODATENDIMENTO: ID único do atendimento
-- - CODLOCAL: local de onde foi processado
-- - TIPO_ATENDIMENTO: sempre "Rematrícula - UNINTA SOBRAL"
-- - ABERTURA: data que foi aberto
-- - FECHAMENTO: data que foi fechado (deve ser 12 ou 13 de julho)
-- - USUARIO_RESPONSAVEL_ATUAL: quem está responsável agora
-- - DATA_MUDANCA_ETAPA: quando foi para a etapa atual
-- - RA: registro do aluno afetado
-- - ALUNO_NOME: nome do aluno
-- - CURSO: qual curso o aluno está
-- - POLO: qual polo/filial


-- ============================================================================
-- PASSO 2: ANALISAR OS RESULTADOS
-- ============================================================================
-- Após executar a consulta, você terá uma lista de atendimentos que:
-- 1. São do tipo 663 (Rematrícula)
-- 2. Foram finalizados em 12 ou 13 de julho de 2026
-- 3. Mostram quem é o responsável atual

-- Procure por:
-- - Atendimentos que foram finalizados por ENGANO (verificar USUARIO_RESPONSAVEL_ATUAL)
-- - Se o usuário não for o esperado, este pode ser um atendimento finalizando errado
-- - A coluna DATA_MUDANCA_ETAPA vai mostrar EXATAMENTE quando foi finalizado


-- ============================================================================
-- PASSO 3: PREPARAR PARA DEVOLUÇÃO (LEITURA APENAS - NÃO EXECUTE)
-- ============================================================================

-- ATENÇÃO: As consultas abaixo são APENAS PARA REFERÊNCIA!
-- Nunca execute INSERT, UPDATE, DELETE ou operações DDL neste banco.
-- A devolução dos atendimentos DEVE SER FEITA PELA INTERFACE DO SISTEMA
-- ou através de um procedimento armazenado autorizado.

-- Exemplo de como seria reabrir (NÃO EXECUTE - SOMENTE PARA REFERÊNCIA):
/*
-- Identifique os CODATENDIMENTO que precisam ser devolvidos
-- Exemplo: CODATENDIMENTO em (12345, 12346, 12347)

-- Você precisaria:
-- 1. Atualizar HATENDIMENTOBASE.CODSTATUS para "ABERTO" ou status adequado
-- 2. Criar novo registro em HHISTORICOETAPASATENDIMENTO com:
--    - CODATENDIMENTO: [ID do atendimento]
--    - COLIGADAETAPAATUAL: 1
--    - CODETAPAATUAL: [nova etapa]
--    - CODATENDENTEATUAL: 40005163 (usuário que receberá)
--    - MUDANCADEETAPA: GETDATE() (data/hora atual)
-- 3. Usar um UPDATE para redirecionar o atendimento
*/


-- ============================================================================
-- PASSO 4: FILTROS ADICIONAIS (OPCIONAL)
-- ============================================================================

-- Se você quer filtrar apenas por um usuário específico que finalizou:
-- Descomente a linha na OPÇÃO 1:
-- AND HHISTORICOETAPASATENDIMENTO.CODATENDENTEATUAL = 40005163

-- Se você quer ver o histórico COMPLETO de um atendimento específico:
SELECT
    HHISTORICOETAPASATENDIMENTO.CODATENDIMENTO,
    HHISTORICOETAPASATENDIMENTO.MUDANCADEETAPA,
    HHISTORICOETAPASATENDIMENTO.CODETAPAATUAL,
    HHISTORICOETAPASATENDIMENTO.CODATENDENTEATUAL,
    HATENDIMENTOBASE.CODTIPOATENDIMENTO,
    HATENDIMENTOBASE.ABERTURA,
    HATENDIMENTOBASE.FECHAMENTO
FROM HHISTORICOETAPASATENDIMENTO WITH (NOLOCK)
    JOIN HATENDIMENTOBASE WITH (NOLOCK)
        ON HATENDIMENTOBASE.CODATENDIMENTO = HHISTORICOETAPASATENDIMENTO.CODATENDIMENTO
WHERE HATENDIMENTOBASE.CODCOLIGADA = 1
  AND HATENDIMENTOBASE.CODTIPOATENDIMENTO = 663
  -- Substitua 12345 pelo CODATENDIMENTO que deseja investigar
  -- AND HHISTORICOETAPASATENDIMENTO.CODATENDIMENTO = 12345
ORDER BY HHISTORICOETAPASATENDIMENTO.MUDANCADEETAPA DESC;


-- ============================================================================
-- PASSO 5: VALIDAÇÃO FINAL
-- ============================================================================

-- Antes de executar qualquer ação, valide:
-- 1. O CODATENDIMENTO realmente existe e é tipo 663
-- 2. O FECHAMENTO está dentro de 12-13 julho
-- 3. O USUARIO_RESPONSAVEL_ATUAL está correto
-- 4. Não há outros atendimentos duplicados para o mesmo aluno

-- Consulta de validação:
SELECT TOP 10
    SALUNO.RA,
    PPESSOA.NOME,
    COUNT(DISTINCT HATENDIMENTOBASE.CODATENDIMENTO) AS TOTAL_ATENDIMENTOS,
    MIN(HATENDIMENTOBASE.ABERTURA) AS PRIMEIRO_ATENDIMENTO,
    MAX(HATENDIMENTOBASE.FECHAMENTO) AS ULTIMO_ATENDIMENTO
FROM HATENDIMENTOBASE WITH (NOLOCK)
    JOIN SATENDIMENTO WITH (NOLOCK)
        ON SATENDIMENTO.CODCOLIGADA    = HATENDIMENTOBASE.CODCOLIGADA
       AND SATENDIMENTO.CODATENDIMENTO = HATENDIMENTOBASE.CODATENDIMENTO
    JOIN SALUNO WITH (NOLOCK)
        ON SALUNO.CODCOLIGADA = SATENDIMENTO.CODCOLIGADA
       AND SALUNO.RA          = SATENDIMENTO.RA
    JOIN PPESSOA WITH (NOLOCK)
        ON PPESSOA.CODIGO = SALUNO.CODPESSOA
WHERE HATENDIMENTOBASE.CODCOLIGADA = 1
  AND HATENDIMENTOBASE.CODTIPOATENDIMENTO = 663
  AND CAST(HATENDIMENTOBASE.FECHAMENTO AS DATE) IN ('2026-07-12', '2026-07-13')
GROUP BY SALUNO.RA, PPESSOA.NOME
HAVING COUNT(DISTINCT HATENDIMENTOBASE.CODATENDIMENTO) > 1
ORDER BY TOTAL_ATENDIMENTOS DESC;


/* ============================================================================
   RESUMO DO PROCESSO
   ============================================================================
   
   1. Execute: consulta_rematricula_663.sql (OPÇÃO 1)
   2. Analise os resultados
   3. Identifique os atendimentos que foram finalizados por engano
   4. CONTATE O SUPORTE/SISTEMA para reabrindo no banco
   5. Transfira para o usuário 40005163 (análise FIES/débito)
   
   NUNCA execute operações de UPDATE/DELETE diretamente!
   Use apenas para CONSULTA/ANÁLISE.
   
   ============================================================================ */
