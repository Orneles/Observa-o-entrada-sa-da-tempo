SELECT 
    nome_visitante,
    COUNT(*) AS total_visitas,
    SUM(
        (strftime('%s', horario_saida) - strftime('%s', horario_entrada))
    ) AS tempo_total_segundos
FROM visitas
WHERE strftime('%Y-%m', horario_entrada) = '2026-01'
AND horario_saida IS NOT NULL
GROUP BY nome_visitante;

CREATE TABLE IF NOT EXISTS moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    apartamento TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS visitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitante_id INTEGER NOT NULL,
    morador_id INTEGER NOT NULL,
    horario_entrada TEXT NOT NULL,
    horario_saida TEXT,
    tempo_permanencia TEXT,
    FOREIGN KEY (visitante_id) REFERENCES visitantes(id),
    FOREIGN KEY (morador_id) REFERENCES moradores(id)
);

SELECT 
    v.nome AS visitante,
    m.nome AS morador,
    m.apartamento,
    vi.horario_entrada,
    vi.horario_saida,
    vi.tempo_permanencia
FROM visitas vi
JOIN visitantes v ON v.id = vi.visitante_id
JOIN moradores m ON m.id = vi.morador_id;

SELECT 
    m.nome,
    COUNT(vi.id) AS total_visitas
FROM visitas vi
JOIN moradores m ON m.id = vi.morador_id
WHERE strftime('%Y-%m', vi.horario_entrada) = '2026-01'
GROUP BY m.nome;



