# frozen_string_literal: true

def to_database(utterances, base)
  puts 'Trwa zapisywanie do bazy danych...'.colorize(:yellow)
  db = SQLite3::Database.new(base)
  make_columns(db)
  fill_columns(utterances, db)
  puts "Zapisano w #{base}.".colorize(:green)
  db
end

def make_columns(base)
  base.execute <<-SQL
  CREATE TABLE IF NOT EXISTS 'wypowiedzi'(
    id INT NOT NULL PRIMARY KEY,
    imie VARCHAR(100),
    opis VARCHAR(300),
    partia VARCHAR(100),
    ocena VARCHAR(25),
    data DATE,
    kategoria_1 TEXT,
    kategoria_2 TEXT)
  SQL
end

def fill_columns(utterances, base) # rubocop:disable Metrics/AbcSize
  utterances.each do |u|
    cat1 = (u.categories[0] ? u.categories[0].to_s : nil)
    cat2 = (u.categories[1] ? u.categories[1].to_s : nil)

    base.execute("INSERT INTO 'wypowiedzi'(
      id, imie, opis, partia, ocena, data, kategoria_1, kategoria_2
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ", [u.id, u.name, u.description, u.party, u.grade, u.date, cat1, cat2])
  end
end
