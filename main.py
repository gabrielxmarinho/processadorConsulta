import parser
# Consulta SQL de exemplo
sql = "SELECT nome FROM pessoas INNER JOIN enderecos ON pessoas.id=enderecos.pessoa_id WHERE idade <! 18"
parser.processarConsulta(sql)