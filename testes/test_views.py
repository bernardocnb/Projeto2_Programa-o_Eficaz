from unittest.mock import patch

import pytest

from servidor import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_index_retorna_mensagem(client):
    resposta = client.get('/')

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        'mensagem': 'API de imoveis funcionando'
    }


@patch('models.listar_imoveis')
def test_listar_todos_os_imoveis(mock_listar, client):
    mock_listar.return_value = [
        {
            'id': 1,
            'logradouro': 'Paulista',
            'tipo_logradouro': 'Avenida',
            'bairro': 'Bela Vista',
            'cidade': 'São Paulo',
            'cep': '01310-100',
            'tipo': 'apartamento',
            'valor': 800000.0,
            'data_aquisicao': '2024-01-15'
        }
    ]

    resposta = client.get('/imoveis')

    assert resposta.status_code == 200
    assert resposta.get_json() == mock_listar.return_value
    mock_listar.assert_called_once_with()


@patch('models.buscar_imovel_por_id')
def test_buscar_imovel_por_id(mock_buscar, client):
    mock_buscar.return_value = {
        'id': 1,
        'logradouro': 'Paulista',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Bela Vista',
        'cidade': 'São Paulo',
        'cep': '01310-100',
        'tipo': 'apartamento',
        'valor': 800000.0,
        'data_aquisicao': '2024-01-15'
    }

    resposta = client.get('/imoveis/1')

    assert resposta.status_code == 200
    assert resposta.get_json() == mock_buscar.return_value
    mock_buscar.assert_called_once_with(1)


@patch('models.buscar_imovel_por_id')
def test_buscar_imovel_inexistente(mock_buscar, client):
    mock_buscar.return_value = None

    resposta = client.get('/imoveis/999')

    assert resposta.status_code == 404
    assert resposta.get_json() == {
        'erro': 'Imóvel não encontrado'
    }
    mock_buscar.assert_called_once_with(999)

@patch('models.buscar_imoveis_por_tipo', create=True)
def test_buscar_imoveis_por_tipo(mock_buscar, client):
    mock_buscar.return_value = [
        {
            'id': 1,
            'logradouro': 'Paulista',
            'tipo_logradouro': 'Avenida',
            'bairro': 'Bela Vista',
            'cidade': 'São Paulo',
            'cep': '01310-100',
            'tipo': 'apartamento',
            'valor': 800000.0,
            'data_aquisicao': '2024-01-15'
        }
    ]

    resposta = client.get('/imoveis?tipo=apartamento')

    assert resposta.status_code == 200
    assert resposta.get_json() == mock_buscar.return_value
    mock_buscar.assert_called_once_with('apartamento')


@patch('models.buscar_imoveis_por_cidade', create=True)
def test_buscar_imoveis_por_cidade(mock_buscar, client):
    mock_buscar.return_value = [
        {
            'id': 2,
            'logradouro': 'Brasil',
            'tipo_logradouro': 'Avenida',
            'bairro': 'Centro',
            'cidade': 'Campinas',
            'cep': '13010-001',
            'tipo': 'casa',
            'valor': 600000.0,
            'data_aquisicao': '2023-06-20'
        }
    ]

    resposta = client.get('/imoveis?cidade=Campinas')

    assert resposta.status_code == 200
    assert resposta.get_json() == mock_buscar.return_value
    mock_buscar.assert_called_once_with('Campinas')

@patch('models.adicionar_imovel', create=True)
def test_adicionar_imovel(mock_adicionar, client):
    novo_imovel = {
        'logradouro': 'Faria Lima',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Itaim Bibi',
        'cidade': 'São Paulo',
        'cep': '04538-132',
        'tipo': 'apartamento',
        'valor': 950000.0,
        'data_aquisicao': '2025-03-10'
    }

    imovel_criado = {
        'id': 3,
        **novo_imovel
    }

    mock_adicionar.return_value = imovel_criado

    resposta = client.post('/imoveis', json=novo_imovel)

    assert resposta.status_code == 201
    assert resposta.get_json() == imovel_criado
    mock_adicionar.assert_called_once_with(novo_imovel)


@patch('models.adicionar_imovel', create=True)
def test_adicionar_imovel_sem_json(mock_adicionar, client):
    resposta = client.post('/imoveis')

    assert resposta.status_code == 400
    assert resposta.get_json() == {
        'erro': 'JSON inválido ou não enviado'
    }

    mock_adicionar.assert_not_called()


@patch('models.adicionar_imovel', create=True)
def test_adicionar_imovel_com_campo_faltando(mock_adicionar, client):
    dados_incompletos = {
        'logradouro': 'Faria Lima',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Itaim Bibi'
    }

    resposta = client.post('/imoveis', json=dados_incompletos)

    assert resposta.status_code == 400
    assert resposta.get_json() == {
        'erro': 'Campos obrigatórios não foram informados'
    }

    mock_adicionar.assert_not_called()