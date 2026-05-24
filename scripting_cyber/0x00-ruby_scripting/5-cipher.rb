
class CaesarCipher
  def initialize(shift)
    @shift = shift
  end

  def encrypt(message)
    cipher(message, @shift)
  end

  def decrypt(message)
    cipher(message, -@shift)
  end

  private

  def cipher(message, shift)
    message.chars.map do |char|
      if char.match?(/[a-z]/)
        ((char.ord - 'a'.ord + shift) % 26 + 'a'.ord).chr
      elsif char.match?(/[A-Z]/)
        ((char.ord - 'A'.ord + shift) % 26 + 'A'.ord).chr
      else
        char
      end
    end.join
  end
end
