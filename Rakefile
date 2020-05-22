namespace :docker do
    desc 'Up Containers'
    task :up do
        sh 'docker-compose ps'
        sh 'docker-compose build --no-cache'
        sh 'docker-compose up -d'
        sh 'docker-compose ps'
    end

    desc 'Dpwm Containers'
    task :down do
        sh 'docker-compose ps'
        sh 'docker-compose down'
        sh 'docker-compose ps'
    end

    desc 'Restart Containers'
    task :restart do
        Rake::Task["docker:down"].invoke
        Rake::Task["docker:up"].invoke
        Rake::Task["docker:test_log"].invoke
    end

    desc 'Check Containers'
    task :ps do
        sh 'docker-compose ps'
    end

    desc 'Login Container'
    task :login do
        sh 'docker-compose exec prometheus /bin/sh'
    end

    desc 'Check Container logs'
    task :log do
        sh 'docker-compose logs prometheus'
    end

    desc 'Test Container logs'
    task :test_log do
        sh 'docker-compose logs prometheus | tail -5 | grep "Server is ready to receive web requests" | wc -l'
        sh 'docker-compose logs prometheus | tail -5 | grep error | wc -l'
    end

    desc 'Clean Container files'
    task :clean do
        sh 'df -h'
        sh 'docker image ls'
        sh 'docker image ls | wc -l'
        sh 'docker system prune --force'
        sh 'df -h'
        sh 'docker image ls'
        sh 'docker image ls | wc -l'
    end

    desc 'Test using pytest'
    task :test do
        sh 'pytest -v --durations=10 --capture=no tests/unit/test_compose.py'
    end
end

namespace :tool do
    desc 'init'
    task :init do
        sh 'python3 -m venv .env'
        puts 'source .env/bin/activate'
        puts 'rake tool:pip'
    end

    desc 'Install package using pip'
    task :pip do
        sh 'pip list'
        sh 'pip install --upgrade pip'
        sh 'pip install -U -r requirements.txt'
        sh 'pip list'
    end
end
