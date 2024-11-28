flag=true

pipeline {
agent any
  parameters{
              //These are types of parameter
                string(name: 'VERSION' ,defaultValue:'',description:'version to deploy on prod')
                choice (name: 'VERSION',choices:['1.1.0','1.2.0','1.3.0'],description:'')
                booleanParam(name:'executeTests',defaultValue: true, description:'')
            }
  environment {
                  NEW_VERSION = '1.3.0'
              }
    
stages {
stage('Build') {
steps {
echo 'Building..'
// Here you can define commands for your build
}
}
stage('Test') {
        when {
                expression {
                              params.executeTests
                            }
        }
steps {
echo 'Testing..'
// Here you can define commands for your tests
}
}
stage('Deploy') {
steps {
echo 'Deploying....'
// Here you can define commands for your deployment
}
}

}

post{
  //the condition here will execute after the build is done
  always {
           //This action will always happen regardless of the result of the build
            echo 'Post build condition running '
         }
  failure {
            //This action will happen only if the build has failed
            echo 'Post Action if build failed'
          }
}
}
