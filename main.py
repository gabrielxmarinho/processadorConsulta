import parser
# Consulta SQL de exemplo
sql = "SELECT nome FROM pessoas INNER JOIN enderecos ON pessoas.id=enderecos.pessoa_id WHERE idade = 18 AND pessoa_id = 2"
parser.processarConsulta(sql)