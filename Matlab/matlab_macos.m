% pulisco variabili
clear;

result_file = fopen('matlab_macos.csv', 'a');
fprintf(result_file,'Software,Sistema,Matrice,Errore Relativo,Tempo Esecuzione (sec),Memoria (MB)\n');

data_path = '/Users/mirkopapadopoli/Code/LinearSolver/MatrixMAT/';
file_dir = dir(fullfile(data_path, '*.mat'));

for i = 1:length(file_dir)
    file_name = file_dir(i).name;
    full_path = strcat(data_path, file_name);
    disp(full_path);

    % carico la matrice
    mat = load(full_path);

    %definisco la matrice A
    A = mat.Problem.A;
    
    % definisco il vettore b come la somma degli elementi di ogni riga della matrice A
    b = sum(A,2);
    
    % start time
    tic;

    % eseguo la decomposizione di Cholesky di A (ottenendo la matrice triangolare inferiore R t.c. A = R*R')
    % viene anche verificato se la matrice è simmetrica e definita positiva
    R = chol(A);
    
    % risolvo il sistema lineare Ax = b utilizzando Cholesky, questo calcolo è
    % specifico per le matrici simmetriche definite positive, a differenza di
    % calcolare "A \ b" che è usato per matrici più generiche.
    x = R\(R'\b);
    
    %end time
    elapsed_time = toc;
  
    % calcolo xe, ovvero la soluzione esatta del sistema lineare A * xe = b
    xe = ones(length(A), 1);
    
    % calcolo l'errore relativo
    err_rel = norm(x - xe) / norm(xe);
    
    disp(['Tempo esecuzione: ', num2str(elapsed_time), ' secondi']);
    disp(['Errore relativo: ', num2str(err_rel)]);
    
    % per visualizzare le variabili e la loro dimensione in memoria
    whos;
    
    size_sum = sum(vertcat(whos('A', 'R', 'b', 'x', 'xe', 'mat').bytes));
    
    % conversione da bytes a mb
    memory = size_sum / 1024^2;

    if ispc
        system = 'Windows';
    elseif ismac
        system = 'MacOS';
    else
        system = 'Linux';
    end
    
    fprintf(result_file,'%s,%s,%s,%g,%0.2f,%0.2f\n','MATLAB',system,file_name, err_rel, elapsed_time, memory);
    clear('A', 'R', 'b', 'x', 'xe', 'mat');

end

fclose(result_file);
