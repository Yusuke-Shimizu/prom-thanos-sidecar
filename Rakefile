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
end
