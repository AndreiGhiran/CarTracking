# CarTracking
## Brief Description
  (to be added)

## Members
### Developers
- Andrei Ghiran (MSD1) (Scrum Master)
- Sergiu Nistor (MSD1)
### Scientific coordinators
- Prof. Dr. Iftene Adrian
- Conf. Dr. Ignat Anca

## Project documentation and State-of-the-art
- https://docs.google.com/document/d/1Mv5c_vVn8FXemM_OQNKI9l1WD4PTJvRDwOpNVZ6OEyM/edit?usp=sharing

## Tasks and Responsibilities Traking
The projects section on the GitHub repository: https://github.com/AndreiGhiran/CarTracking/projects/1

## Lab 4 contributions
**Andrei Ghiran:**
- implemented TrafficParticipant basic classe and decorators for basic AOP functionality
- implemented CarRequestFullfilmentAuthority basic classe and decorators for basic AOP functionality

**Sergiu Nistor:**
- database initialization script (*DB/init_script.sql*)
- data processing authority logic:
    - logic for common database operations (*DataProcessing/Authority/src/logic/DatabaseHandler.py*)
    - logic for UDP connection with the traffic cameras (*DataProcessing/Authority/src/logic/UDPEndpoint.py*)
    - logic for data processing:
        - algorithm base class (*DataProcessing/Authority/src/logic/algorithms/AbstractAlgorithm.py*)
        - logic for the data processing entity (*DataProcessing/Authority/src/logic/DataProcessingEntity.py*), which makes use of the following algorithms:
            - object detection algo using a pre-trained Faster Residual Convolutional Neural Network (*DataProcessing/Authority/src/logic/algorithms/ObjectDetection.py*)
            - depth estimation algo using MiDaS, a pre-trained Residual Convolutional Neural Network (*DataProcessing/Authority/src/logic/algorithms/DepthEstimation.py*)

**Next steps:**
- write the data processing authority dispatcher (**Asignee: Sergiu**)
- continue writing the logic for the data processing entity (**Asignee: Sergiu**)

## Lab 5 contributions
**Sergiu Nistor:**
- write the data processing authority dispatcher
- continue writing the logic for the data processing entity

**Next steps:**
- Unit tests (mock external dependencies; only test on discrete components/classes; Mockito: https://pypi.org/project/mockito/)
