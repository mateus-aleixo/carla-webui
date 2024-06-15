describe('CARLA Web UI Tests', () => {
    beforeEach(() => {
        // Intercept API calls and mock responses if necessary
        cy.intercept('GET', '/api/carla/world_info', {
            fixture: 'world_info.json',
        });
        cy.intercept('GET', '/api/carla/map_info', {
            fixture: 'map_info.json',
        });
        cy.intercept('GET', '/api/carla/ego/sensors', {
            fixture: 'sensors.json',
        });
        cy.intercept('DELETE', '/api/carla/destroy/all', {
            body: { success: true },
        });
        cy.visit('/');
    });

    it('should display world info correctly', () => {
        cy.contains('Map: Town10');
        cy.contains('Precipitation: 0');
        cy.contains('Wind Intensity: 0');
        cy.contains('Number of Actors: 0');
    });

    it('should display ego sensors correctly', () => {
        cy.get('.ego-sensors').should('exist');
        cy.contains('Collision History:');
        cy.contains('GNSS Data:');
        cy.get('.ego-sensors img').should('have.attr', 'src').should('include', 'data:image/png;base64');
    });

    it('should remove all actors when button is clicked', () => {
        cy.get('button').contains('Remove All Actors').click();
        cy.get('.MuiAlert-message').should('not.exist');
    });
});