# frozen_string_literal: true

# NOTE: As all the scrapped data is in Polish, I decide without any hesitation
#   to keep the column names of the generated database in Polish as well, despite
#   English being standard for variable names. Moreover, the entire program used
#   to have variable names in Polish, but that might have been 'a little bit'
#   too much. Just saying that strings are intended to bee in Polish as well.

# NOTE2: The scrapped website is demagog.org.pl, which is a Polish fact-checking
#   site which is quite useful for debunking fake news or checking whether our
#   'beloved' politicians tell us THE truth, or THEIR OWN 'truth'.

# If you somehow find this code useful, you are free to modify, improve or use it
#   as long as it is for harmless purposes. The code is provided as it is and I
#   held no responsibility for your actions (such as using it to flood the site's
#   server or whatever else...). Not cool.

require 'open-uri'
require 'pry'
require 'colorize'
require 'nokogiri'
require 'sqlite3'
require 'date'

require_relative 'scrapping'
require_relative 'utterance'
require_relative 'sqlite3_interface'

Selector = Struct.new(:data, :grade, :date_and_categories)

selectors = Selector.new(
  ':nth-child(1) > div:nth-child(1) > div:nth-child(1) > a > div',
  ':nth-child(1) > div:nth-child(2) > div:nth-child(2)',
  ':nth-child(2)'
)

utterances = []
process_all_pages(utterances, selectors)

# I'm aware it would be a better idea to start from the last utterance from the last page
#   than reversing the entire list of about 4.1k utterances (11.11.2020) in order to assign
#   them ids starting from the oldest utterance. Current implementation might be seen as a
#   prototype, though it's good enough to satisfy my own needs and that's why I'm leaving
#   it as it is now.
utterances.reverse!.each_with_index { |w, i| w.id = i + 1 }

utterances.each(&:to_pretty_s)

base = 'demagog.db'

begin
  db = SQLite3::Database.open(base)
  old_entry_count = db.execute('SELECT COUNT(id) FROM wypowiedzi')[0][0]
  db.close
rescue SQLite3::SQLException
  old_entry_count = 0
end

File.delete(base) if File.exist?(base)
to_database(utterances, base)

db = SQLite3::Database.open(base)
new_entry_count = db.execute('SELECT COUNT(id) FROM wypowiedzi')[0][0]
db.close

print "Dodano #{new_entry_count - old_entry_count} wypowiedzi. ".colorize(:yellow)
puts "(Wzrost z #{old_entry_count} do #{new_entry_count}.)".colorize(:yellow)
