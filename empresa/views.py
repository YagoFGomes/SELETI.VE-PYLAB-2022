from django.shortcuts import render, redirect, get_object_or_404
from .models import Tecnologias, Empresa, Vagas
from django.contrib import messages
from django.contrib.messages import constants

def NovaEmpresa(request):
    if request.method == "GET":
        tecnologias = Tecnologias.objects.all()
        return render(request, 'nova_empresa.html', {'tecnologias': tecnologias})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        nicho = request.POST.get('nicho')
        caracteristicas = request.POST.get('caracteristicas')
        tecnologias = request.POST.getlist('tecnologias')
        logo = request.FILES.get('logo')

        if (len(nome.strip()) == 0 or len(email.strip()) == 0 or len(cidade.strip()) == 0 or len(endereco.strip()) == 0 or len(nicho.strip()) == 0 or len(caracteristicas.strip()) == 0 or (not logo)): 
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/home/nova_empresa')

        if logo.size > 100_000_000:
            messages.add_message(request, constants.ERROR, 'A logo da empresa deve ter menos de 10MB')
            return redirect('/home/nova_empresa')

        if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
            messages.add_message(request, constants.ERROR, 'Nicho de mercado inválido')
            return redirect('/home/nova_empresa')

        empresa = Empresa(logo=logo,
                        nome=nome,
                        email=email,
                        cidade=cidade,
                        endereco=endereco,
                        nicho_mercado=nicho,
                        caracteristica_empresa=caracteristicas)
        empresa.save()
        empresa.tecnologias.add(*tecnologias) # Salvando o método ManyToMany
        empresa.save()
        messages.add_message(request, constants.SUCCESS, 'Empresa cadastrada com sucesso')
        return redirect('/home/empresas')

def Empresas(request):
    technologias_filtrar = request.GET.get('tecnologias')
    nome_filtrar = request.GET.get('nome')

    todas_empresas = Empresa.objects.all()

    if technologias_filtrar:
        todas_empresas = todas_empresas.filter(tecnologias = technologias_filtrar)
    
    if nome_filtrar:
        todas_empresas = todas_empresas.filter(nome__icontains = nome_filtrar)

    tecnologias = Tecnologias.objects.all()
    return render(request, 'empresa.html', {'empresas': todas_empresas, 'tecnologias': tecnologias})

def EmpresaUnica(request, id):
    empresa_unica = get_object_or_404(Empresa, id=id)
    empresas = Empresa.objects.all()
    tecnologias = Tecnologias.objects.all()
    vagas = Vagas.objects.filter(empresa_id=id)
    return render(request, 'empresa_unica.html', {'empresa': empresa_unica,
                                            'tecnologias': tecnologias,
                                            'empresas': empresas,
                                            'vagas': vagas})


def ExcluirEmpresa(request, id):
    empresa = Empresa.objects.get(id=id)
    empresa.delete()
    messages.add_message(request, constants.SUCCESS, 'Empresa removida com sucesso')
    return redirect('/home/empresas')