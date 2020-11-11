# frozen_string_literal: true

def find_date(response, selector)
  return nil unless response.css("#{selector} > span:first-child")[0]

  response.css("#{selector} > span:first-child")[0].text
end

def find_categories(response, selector)
  return nil unless response.css("#{selector} > a")

  categories = []
  response.css("#{selector} > a > span:first-child").each do |cat|
    next if cat.text == ''

    categories << cat.text.to_sym
  end
  categories
end

# Gets name of a politician.
def find_name(response, selector)
  return nil unless response.css("#{selector} > p.mb-0")[0]

  response.css("#{selector} > p.mb-0")[0].text
end

# Gets description/role of a politician e.g. 'president', 'PM', 'MOP'
def find_description(response, selector)
  return nil unless response.css("#{selector} > p.mb-0")[1]

  response.css("#{selector} > p.mb-0")[1].text.gsub(',', '')
end

# Gets the party of a politician
def find_party(response, selector)
  return nil unless response.css("#{selector} > p.partia")[0]

  response.css("#{selector} > p.partia")[0].text
end

# Gets the grade of a politician's speech: truth/lie/manipulation/unverifiable
def find_grade(response, selector)
  return nil unless response.css(selector.to_s)[0]

  response.css(selector)[0].text.strip!
end

def process_data(response, selectors, utterances)
  data = {
    name: find_name(response, selectors.data),
    description: find_description(response, selectors.data),
    party: find_party(response, selectors.data),
    grade: find_grade(response, selectors.grade),
    date: find_date(response, selectors.date_and_categories),
    categories: find_categories(response, selectors.date_and_categories)
  }
  utterances << Utterance.new(data)
end

def process_utterance(doc, utterances, selectors)
  id = 2 # Counting starts from 1, the first child does not contain any information.
  loop do
    response = doc.css("#response > div:nth-child(#{id})")
    break if response.empty?

    process_data(response, selectors, utterances)
    id += 1
  end
end

def process_all_pages(utterances, selectors) # rubocop:disable Metrics/MethodLength
  page = 1
  loop do
    begin
      doc = Nokogiri::HTML(URI.open("https://demagog.org.pl/wypowiedzi/page/#{page}/"))
      puts "Przetwarzanie strony #{page}. Proszę czekać...".colorize(:blue)
      process_utterance(doc, utterances, selectors)
      page += 1
    rescue OpenURI::HTTPError
      puts "Program zakończył swoje działanie na stronie #{page}.".colorize(:yellow)
      break
    end
  end
end
