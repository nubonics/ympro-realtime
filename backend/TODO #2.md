# TODO # 2
- [ ] **Task Management System**
  - [ ] !!! Pagination of hostler tasks !!!
  - [ ] Transfer from hostler to workbasket
  - [ ] Transfer from hostler to hostler
  - [ ] Each task
    - [ ] Get the zone for each task
    - [x] Get the context_page for each task
    - [x] Get the strIndexList for each task
    - [ ] Get the activity_params for each task
    - [x] Get the team_members_pd_key for each task
    - [ ] Get the pzuiactionzzz for each task

  - ✅❌ Transfer from workbasket to hostler
    - works, but using playwright... so not the best 
    - need to switch to async httpx
    - playwright doesnt play nicely with fastapi
    - cant use --reload, and makes weird errors happen


- [ ] Rules
  - [x] mty van counts as a duplicate, it should not
  - [x] dont delete door 0 tasks
  - [x] dont delete NOT IN PLAN tasks
  - [x] dont delete OB tasks
  - [x] check for duplicate trailer # with different door #
  - [x] check for duplicate door # with same trailer #
  - [x] check for duplicate door and trailer #
  - [ ] check for boxtruck tasks [ pulls ]
    - [x] delete SPEC tasks
    - ✅ delete 19xxx tasks
    - [ ] delete 10xxx tasks
  - ✅ check for preventive maintenance tasks


- [ ] Pubsub
  - [ ] Add pubsub to the backend
  - [ ] Add pubsub to the frontend
  - [ ] Add pubsub to the worker
  - [ ] Add pubsub to the poller
  - [ ] Add pubsub to the api layer


- [ ] Test
  - [ ] Add tests for the task management system
  - [ ] Add tests for the pubsub system
  - [ ] Add tests for the worker
  - [ ] Add tests for the poller
  - [ ] Add tests for the api layer


- [ ] Documentation
  - [ ] Add documentation for the task management system
  - [ ] Add documentation for the pubsub system
  - [ ] Add documentation for the worker
  - [ ] Add documentation for the poller
  - [ ] Add documentation for the api layer


- [ ] Refactor
  - [ ] Refactor the task management system
  - [ ] Refactor the pubsub system
  - [ ] Refactor the worker
  - [ ] Refactor the poller
  - [ ] Refactor the api layer


- [ ] Deployment
  - [ ] Add deployment scripts for the task management system
  - [ ] Add deployment scripts for the pubsub system
  - [ ] Add deployment scripts for the worker
  - [ ] Add deployment scripts for the poller
  - [ ] Add deployment scripts for the api layer


- [ ] Monitoring
  - [ ] Add monitoring for the task management system
  - [ ] Add monitoring for the pubsub system
  - [ ] Add monitoring for the worker
  - [ ] Add monitoring for the poller
  - [ ] Add monitoring for the api layer


- [ ] Performance
  - [ ] Add performance tests for the task management system
  - [ ] Add performance tests for the pubsub system
  - [ ] Add performance tests for the worker
  - [ ] Add performance tests for the poller
  - [ ] Add performance tests for the api layer


- [ ] Security
  - [ ] Add security tests for the task management system
  - [ ] Add security tests for the pubsub system
  - [ ] Add security tests for the worker
  - [ ] Add security tests for the poller
  - [ ] Add security tests for the api layer

    
- [ ] Scalability
  - [ ] Add scalability tests for the task management system
  - [ ] Add scalability tests for the pubsub system
  - [ ] Add scalability tests for the worker
  - [ ] Add scalability tests for the poller
  - [ ] Add scalability tests for the api layer
  

- [ ] Reliability
  - [ ] Add reliability tests for the task management system
  - [ ] Add reliability tests for the pubsub system
  - [ ] Add reliability tests for the worker
  - [ ] Add reliability tests for the poller
  - [ ] Add reliability tests for the api layer


- [ ] Usability
  - [ ] Add usability tests for the task management system
  - [ ] Add usability tests for the pubsub system
  - [ ] Add usability tests for the worker
  - [ ] Add usability tests for the poller
  - [ ] Add usability tests for the api layer