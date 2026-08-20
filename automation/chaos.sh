#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

cat << 'EOF'
╔════════════════════════════════════════════════════════╗
║           🔮 CHAOS BUTTON v1.0 🔮                       ║
║         "Because breaking things is fun!"              ║
╚════════════════════════════════════════════════════════╝
EOF

echo ""
echo -e "${YELLOW}Available chaos actions:${NC}"
echo ""
echo -e "  ${CYAN}[1]${NC} Stop FastAPI (the app itself)"
echo -e "  ${CYAN}[2]${NC} Stop PostgreSQL (the database)"
echo -e "  ${CYAN}[3]${NC} Break DATABASE_PASSWORD env var"
echo -e "  ${CYAN}[4]${NC} Stop Prometheus (metrics)"
echo -e "  ${CYAN}[5]${NC} Break Nginx config (proxy)"
echo -e "  ${CYAN}[6]${NC} Delete test data (simulate data loss)"
echo -e "  ${CYAN}[7]${NC} Stop Grafana (dashboards)"
echo -e "  ${CYAN}[8]${NC} Random chaos (surprise me!)"
echo -e "  ${CYAN}[0]${NC} Exit - I'm too scared!"
echo ""

echo -e "${YELLOW}Choose your chaos (0-8): ${NC}"
read -r choice

case "$choice" in
    1)
        echo -e "${RED}💀 Stopping FastAPI...${NC}"
        docker stop fastapi-app 2>/dev/null || echo "Container not running"
        echo -e "${GREEN}✅ FastAPI stopped!${NC}"
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check if container is running with: docker ps -a"
        ;;
    2)
        echo -e "${RED}💀 Stopping PostgreSQL...${NC}"
        docker stop postgres-db 2>/dev/null || echo "Container not running"
        echo -e "${GREEN}✅ PostgreSQL stopped!${NC}"
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check: docker logs postgres-db"
        ;;
    3)
        echo -e "${RED}💀 Breaking DATABASE_PASSWORD...${NC}"
        cp app/.env "app/.env.backup.$(date +%s)"
        sed -i 's/DATABASE_PASSWORD=password/DATABASE_PASSWORD=wrongpassword/' app/.env
        echo -e "${GREEN}✅ DATABASE_PASSWORD corrupted!${NC}"
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check .env file, then restore with: cp app/.env.backup.* app/.env"
        ;;
    4)
        echo -e "${RED}💀 Stopping Prometheus...${NC}"
        docker stop prometheus 2>/dev/null || echo "Container not running"
        echo -e "${GREEN}✅ Prometheus stopped!${NC}"
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check: docker ps | grep prometheus"
        ;;
    5)
        echo -e "${RED}💀 Breaking Nginx config...${NC}"
        if [ -f "nginx/nginx.conf" ]; then
            cp nginx/nginx.conf "nginx/nginx.conf.backup.$(date +%s)"
            echo "invalid_syntax {" > nginx/nginx.conf
            echo -e "${GREEN}✅ Nginx config broken!${NC}"
        else
            echo -e "${YELLOW}⚠ Nginx config not found at nginx/nginx.conf${NC}"
        fi
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check nginx error logs, restore with: nginx/nginx.conf.backup.*"
        ;;
    6)
        echo -e "${RED}💀 Deleting test data...${NC}"
        docker exec postgres-db psql -U admin -d company -c "DROP TABLE IF EXISTS users CASCADE;" 2>/dev/null || echo "Failed or table doesn't exist"
        echo -e "${GREEN}✅ Test data deleted!${NC}"
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check tables: docker exec postgres-db psql -U admin -d company -c '\\dt'"
        ;;
    7)
        echo -e "${RED}💀 Stopping Grafana...${NC}"
        docker stop grafana 2>/dev/null || echo "Container not running"
        echo -e "${GREEN}✅ Grafana stopped!${NC}"
        echo ""
        echo -e "${YELLOW}Investigation hint:${NC} Check: docker ps | grep grafana"
        ;;
    8)
        echo -e "${BLUE}🎲 Rolling the dice...${NC}"
        sleep 1
        random=$((RANDOM % 7 + 1))
        echo -e "${CYAN}Chaos #${random} incoming!${NC}"
        echo ""
        $0  # Recursively call self with random choice
        ;;
    0)
        echo -e "${GREEN}👋 Smart choice. Chaos deferred.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice! Try again.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BOLD}════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}🔍 Now it's your turn to investigate and fix!${NC}"
echo -e "${BOLD}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Common investigation commands:${NC}"
echo "  docker ps -a                    # See all containers"
echo "  docker logs <container>         # Check container logs"
echo "  docker-compose -f docker/docker-compose.yml logs"
echo "  curl http://localhost:8000      # Test API"
echo "  curl http://localhost:80        # Test Nginx"
echo ""
echo -e "${GREEN}Good luck, chaos engineer! 🔧${NC}"