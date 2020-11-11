# frozen_string_literal: true

# xDDDDD
class Utterance
  attr_reader :name, :description, :party, :grade, :date, :categories
  attr_accessor :id

  def initialize(data)
    @name = data[:name]
    @description = data[:description]
    @party = data[:party]
    @grade = data[:grade]
    @date = Date.strptime(data[:date], '%d.%m.%Y').to_s
    @categories = data[:categories]
    @id = nil
  end

  def to_pretty_s
    print_id
    print_name
    print_description
    print_party
    print_grade
    print_date
    print_categories
    puts "\n"
  end

  private
  def grade_color(grade)
    case grade[0].upcase
    when 'P' then :green
    when 'M' then :yellow
    when 'F' then :red
    when 'N' then :blue
    else :black
    end
  end

  def print_id
    id ? (print "#{id}: ".colorize(:red)) : (print 'Brak id: '.colorize(:black))
  end

  def print_name
    name ? (print "#{name} ".colorize(:magenta)) : (print 'Brak imienia '.colorize(:black))
  end

  def print_description
    description ? (print "#{description} ".colorize(:yellow)) : (print 'Brak opisu '.colorize(:black))
  end

  def print_party
    party ? (print "#{party} ".colorize(:cyan)) : (print 'Brak partii '.colorize(:black))
  end

  def print_grade
    grade ? (print "#{grade} ".colorize(grade_color(grade))) : (print 'Brak oceny '.colorize(:black))
  end

  def print_date
    date ?  (print "#{date} ".colorize(:magenta)) : (print 'Brak daty '.colorize(:black))
  end

  def print_categories
    return print 'Brak kategorii '.colorize(:black) if categories.empty?

    categories.each { |cat| print "#{cat}; ".colorize(:green) }
    nil # prevents printing the 'categories' array
  end
end
