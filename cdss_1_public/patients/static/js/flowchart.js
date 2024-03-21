// flowchart.js
document.addEventListener('DOMContentLoaded', function() {
    function visualizeFlowchart(containerId, decisionLogic) {
        jsPlumb.ready(function() {
            var instance = jsPlumb.getInstance({
                DragOptions: { cursor: 'pointer', zIndex: 2000 },
                ConnectionOverlays: [
                    ['Arrow', { location: 1, visible: true, width: 11, length: 11 }]
                ],
                Container: containerId
            });

            // Helper function to create a node
            function createNode(id, label, x, y) {
                var node = document.createElement('div');
                node.id = id;
                node.innerHTML = label;
                node.style.left = x + 'px';
                node.style.top = y + 'px';
                node.classList.add('flowchart-node');
                instance.getContainer().appendChild(node);
                instance.draggable(node, { containment: true });
                return node;
            }

            // Helper function to connect nodes
            function connectNodes(sourceId, targetId) {
                instance.connect({ source: sourceId, target: targetId, anchors: ['Right', 'Left'], endpoint: 'Blank' });
            }

            // Create nodes and connections based on decision logic
            for (var i = 0; i < decisionLogic.length; i++) {
                var decisionPoint = decisionLogic[i];
                var currentNode = createNode('node' + i, decisionPoint.label, 100 * i, 100);

                for (var j = 0; j < decisionPoint.answers.length; j++) {
                    var answerNode = createNode('node' + i + '_' + j, decisionPoint.answers[j], 100 * i, 200 * (j + 1));
                    connectNodes('node' + i, 'node' + i + '_' + j);
                }
            }
        });
        }
    // Call the function to visualize the flowchart
    visualizeFlowchart();
    });
